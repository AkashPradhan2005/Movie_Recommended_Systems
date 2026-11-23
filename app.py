import os
import html
import pickle

import pandas as pd
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# --------------------------------------------------
# 0. Page config (must be the first Streamlit call)
# --------------------------------------------------
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide",
)


# --------------------------------------------------
# 1. Load custom CSS from style.css
# --------------------------------------------------
def load_css(file_name="style.css"):
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# --------------------------------------------------
# 2. Load data
# --------------------------------------------------
@st.cache_resource
def load_data():
    movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return pd.DataFrame(movies_dict), similarity


movies, similarity = load_data()


# --------------------------------------------------
# 3. TMDB API
# --------------------------------------------------
# Keep the key out of the code: use an environment variable or .streamlit/secrets.toml
def get_api_key():
    key = os.environ.get("af42fa0676090a42d1b4bb2325cb5067")
    if key:
        return key
    try:
        return "af42fa0676090a42d1b4bb2325cb5067"
    except Exception:
        return ""


TMDB_API_KEY = get_api_key()

session = requests.Session()
retry = Retry(
    total=3,
    connect=3,
    read=2,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
session.mount("https://", HTTPAdapter(max_retries=retry))


@st.cache_data(show_spinner=False, ttl=86400)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    try:
        response = session.get(url, params=params, timeout=(5, 20))
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path.lstrip("/")
        return None
    except requests.exceptions.RequestException as e:
        print(f"TMDB API Error for movie ID {movie_id}: {e}")
        return None


# --------------------------------------------------
# 4. Recommendation logic
# --------------------------------------------------
def recommend(movie, n=5):
    if movie not in movies["title"].values:
        return [], []

    pos = movies.index[movies["title"] == movie][0]
    ranked = sorted(enumerate(similarity[pos]), reverse=True, key=lambda x: x[1])
    ranked = [i for i in ranked if i[0] != pos][:n]

    titles, posters = [], []
    for idx, _ in ranked:
        row = movies.iloc[idx]
        titles.append(row["title"])
        posters.append(fetch_poster(row["movie_id"]))
    return titles, posters


def movie_card(rank, title, poster):
    safe_title = html.escape(title)
    if poster:
        img = f'<div class="poster-wrap"><img src="{poster}" alt="{safe_title}"></div>'
    else:
        img = '<div class="no-poster">Poster not available</div>'
    delay = (rank - 1) % 5 * 0.12
    return f"""
    <div class="movie-card" style="animation-delay:{delay}s">
        <span class="rank">#{rank}</span>
        {img}
        <div class="movie-title">{safe_title}</div>
    </div>
    """


# --------------------------------------------------
# 5. UI
# --------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <h1>🎬 CineMatch</h1>
        <p>Pick a movie you love and discover similar ones instantly.</p>
        <div class="pills">
            <span class="pill">🎞️ {len(movies):,} movies</span>
            <span class="pill">🤖 Content-based filtering</span>
            <span class="pill">⚡ Instant results</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not TMDB_API_KEY:
    st.error(
        "TMDB API key not found. Set the `TMDB_API_KEY` environment variable "
        "or add it to `.streamlit/secrets.toml`."
    )

left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="panel-label">Choose a movie</div>', unsafe_allow_html=True)
    selected_movie_name = st.selectbox(
        "Select a movie:", movies["title"].values, label_visibility="collapsed"
    )
with right:
    st.markdown('<div class="panel-label">Number of results</div>', unsafe_allow_html=True)
    num_recs = st.slider("Number of recommendations", 3, 10, 5, label_visibility="collapsed")

if st.button("✨ Recommend"):
    with st.spinner("Finding similar movies..."):
        recommendations, posters = recommend(selected_movie_name, num_recs)

    if recommendations:
        st.markdown(
            f'<div class="section-title">Because you liked <span>{html.escape(selected_movie_name)}</span></div>',
            unsafe_allow_html=True,
        )

        per_row = 5
        for start in range(0, len(recommendations), per_row):
            chunk = list(
                zip(
                    range(start + 1, start + per_row + 1),
                    recommendations[start:start + per_row],
                    posters[start:start + per_row],
                )
            )
            cols = st.columns(per_row)
            for col, (rank, title, poster) in zip(cols, chunk):
                with col:
                    st.markdown(movie_card(rank, title, poster), unsafe_allow_html=True)
            st.write("")
    else:
        st.warning("No recommendations found!")

st.markdown(
    '<div class="footer">Built with Streamlit · Movie data and posters from TMDB</div>',
    unsafe_allow_html=True,
)
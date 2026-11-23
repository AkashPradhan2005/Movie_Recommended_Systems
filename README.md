# 🎬 CineMatch – Movie Recommendation System

**CineMatch** is a content-based Movie Recommendation System that helps users discover movies similar to their selected movie. It analyzes movie information such as genres, keywords, overview, cast, and director to identify and recommend similar movies.

The application is built using Machine Learning techniques and Streamlit, with TMDB API integration for fetching movie posters.

## 🚀 Project Overview

The main objective of this project is to build a movie recommendation engine that suggests relevant movies based on content similarity rather than user ratings or preferences.

Users can select a movie, choose the number of recommendations, and instantly discover similar movies through an interactive web application.

## ✨ Features

- Content-based movie recommendations.
- Movie similarity calculation using Cosine Similarity.
- Text feature extraction using CountVectorizer.
- Text preprocessing and stemming.
- Interactive movie selection.
- Customizable number of recommendations.
- Movie poster integration using TMDB API.
- Responsive interface built with Streamlit.
- Cached data loading and API responses for improved performance.

## 🛠️ Technologies & Libraries Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | CountVectorizer and Cosine Similarity |
| NLTK | Text preprocessing and stemming |
| Streamlit | Web application development |
| Pickle | Model and data serialization |
| Requests | TMDB API integration |
| HTML & CSS | Custom UI styling |
| Jupyter Notebook | Model development and experimentation |

## 📂 Project Structure

```text
Movie_Recommended_Systems/
│
├── app.py
├── movies.ipynb
├── movie_dict.pkl
├── movies.pkl
├── requirements.txt
├── Procfile
├── setup.sh
├── style.css
├── .gitignore
│
├── tmdb_5000_movies.csv
└── tmdb_5000_credits.csv
```

**Note:** The `similarity.pkl` model artifact is not included in this repository because it exceeds GitHub's individual file size limit. It must be obtained separately before running the application.

## ⚙️ Machine Learning Workflow

### 1. Data Collection
- Loaded TMDB Movies and Credits datasets.
- Merged both datasets using the movie title.

### 2. Data Preprocessing
- Selected relevant movie features.
- Handled missing values.
- Extracted genres, keywords, cast, and director information.
- Converted movie overview text into tokens.
- Removed spaces from selected feature values.

### 3. Feature Engineering
Combined the following features into a single `tags` column:

- Movie Overview
- Genres
- Keywords
- Top 3 Cast Members
- Director

### 4. Text Vectorization
- Applied Porter Stemming using NLTK.
- Used CountVectorizer for text vectorization.
- Limited the vocabulary to 5,000 features.
- Removed English stop words.

### 5. Similarity Calculation
- Applied Cosine Similarity to calculate similarity between movie vectors.
- Ranked movies based on similarity scores.
- Retrieved the top recommended movies.

### 6. Application Development
- Built an interactive interface using Streamlit.
- Integrated TMDB API to fetch movie posters.
- Displayed recommendations with movie titles and posters.

## 📊 Dataset Information

This project uses the TMDB 5000 Movie Dataset.

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

Dataset source: [TMDB 5000 Movie Dataset – Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AkashPradhan2005/Movie_Recommended_Systems.git
```

### 2. Navigate to the Project Directory

```bash
cd Movie_Recommended_Systems
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Environment

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure TMDB API Key

Create a `.streamlit/secrets.toml` file:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

Alternatively, configure the `TMDB_API_KEY` environment variable.

Never commit API keys or other credentials to GitHub.

### 7. Add Required Model Files

Place the required serialized model artifacts in the project directory:

- `movie_dict.pkl`
- `similarity.pkl`

### 8. Run the Application

```bash
python -m streamlit run app.py
```

Open your browser:

```text
http://localhost:8501
```

## 🖥️ Application Preview

<img width="1739" height="786" alt="Project" src="https://github.com/user-attachments/assets/93df282f-6edf-401b-8f54-6fe9ada882bc" />


## 🌐 Live Demo

 Local URL: http://localhost:8501

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Data preprocessing and feature engineering.
- Natural Language Processing fundamentals.
- Text vectorization and stemming.
- Content-based recommendation systems.
- Similarity-based machine learning techniques.
- Model serialization using Pickle.
- Building interactive ML applications using Streamlit.
- Integrating third-party APIs.

## 👨‍💻 Author

**Akash Pradhan**

- GitHub: [AkashPradhan2005](https://github.com/AkashPradhan2005)

---

*Developed as a Machine Learning project to explore content-based recommendation systems and practical ML application development.*

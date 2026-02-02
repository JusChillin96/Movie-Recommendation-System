# 🎬 Movie Matcher: Interactive Recommendation Engine

### A production-ready Movie Recommender built with Python, Streamlit, and Fuzzy String Matching.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat&logo=streamlit)
![Matching](https://img.shields.io/badge/Search-FuzzyWuzzy-green)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)

## 📌 Project Overview
Most recommendation systems fail when a user makes a typo or gets the title slightly wrong. This project solves that by combining **Item-Based Collaborative Filtering** with **Fuzzy String Matching**, wrapped in a clean, interactive **Streamlit web interface**.

Users can type in a movie (even with typos like "the marix") and receive 10 highly correlated recommendations based on the behavior of over 600 real users.

## 🚀 Live Demo
**[[INSERT YOUR STREAMLIT CLOUD URL HERE](https://recommend-me-some-movies.streamlit.app/)]**

## 📂 Dataset
The project uses the **MovieLens Small Dataset** (100k ratings, 9k movies).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGtpmzcwrVYQq3-VCXtI0bsco0Z_RjTupdbinn8S6xWe8EuIDhyHs3aaEO_eeYWrUiNEMMosLsHtf7MPYEw4iaRHRRYxNBsAD4uZeONrY7u4gHhJTOM1sNEtCnTcyI26kEGbYLb2w%3D%3D)]
*   `movies.csv`: Contains movie titles and genres.
*   `ratings.csv`: Contains user ratings on a 1-5 scale.

## 🛠️ Key Advancements
### 1. Robust Search (Fuzzy Matching)
I implemented `thefuzz` library using the `token_sort_ratio` algorithm. This allows the system to:
*   Handle **Typos** (e.g., "Incepton" -> "Inception").
*   Ignore **Word Order** (e.g., "Matrix The" -> "The Matrix").
*   Ignore **Case Sensitivity**.

### 2. Collaborative Filtering Engine
The engine calculates similarity using **Pearson Correlation** between user-rating vectors. To ensure high-quality suggestions, I implemented a **Popularity Threshold**, filtering out any movies with fewer than 50 ratings to remove statistical noise.

### 3. Full Deployment
The model is moved out of a Jupyter Notebook and into a multi-threaded web app using **Streamlit**, allowing any user to interact with the engine in real-time.

## ⚙️ Tech Stack
*   **Backend:** Python, Pandas, NumPy
*   **Matching:** TheFuzz (Levenshtein Distance)
*   **UI/Frontend:** Streamlit
*   **Performance:** `python-Levenshtein` for high-speed string calculations.

## 📂 Project Structure
*   `app.py`: The main Streamlit application script.
*   `requirements.txt`: List of dependencies for cloud deployment.
*   `movies.csv` / `ratings.csv`: The core data files.

## 💻 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/JusChillin96/Movie-Recommendation-System.git

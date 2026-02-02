# 🎬 Movie Matcher: Hybrid Recommendation Engine

### A high-performance web application that combines Collaborative Filtering and Content-Based logic to provide intelligent movie suggestions.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat&logo=streamlit)
![Algorithm](https://img.shields.io/badge/Algorithm-Hybrid--Collaborative-orange)
![Performance](https://img.shields.io/badge/Speed-Optimized-brightgreen)

## 📌 Project Overview
Purely "social" recommendation systems often suffer from statistical noise—recommending random movies just because one user watched both. This project implements a **Hybrid Engine** that balances user-rating correlations with genre similarity to ensure results are both mathematically sound and contextually relevant.

## 🚀 Live Demo
**[[INSERT YOUR STREAMLIT CLOUD URL HERE](https://recommend-me-some-movies.streamlit.app/)]**

## 🛠️ Engineering Highlights

### 1. Hybrid Recommendation Logic
Most beginners use only one method. This system uses two:
*   **Collaborative Filtering:** Uses Pearson Correlation to find movies that "behave" like the input based on 100,000+ user ratings.
*   **Content-Based Boosting:** Applies a weighted "Genre Boost" by calculating the intersection of genre sets. This ensures that searching for a superhero movie actually returns superhero movies, even if the rating data is sparse.

### 2. High-Performance Optimization
To ensure a "lag-free" user experience on the web:
*   **Matrix Shrinking:** I reduced the computational search space by 95% (from 9,000 to ~450 columns) by pre-filtering for high-confidence (50+ ratings) candidates.
*   **Data Caching:** Utilized `@st.cache_data` to store heavy pivot tables in memory, reducing load times to near-instant for subsequent searches.
*   **Efficient String Logic:** Replaced real-time string splitting with pre-calculated Genre Sets to minimize CPU overhead.

### 3. "Indestructible" Search Box
Integrated `thefuzz` with a `token_sort_ratio` scorer. This allows the system to remain robust against:
*   **Typos:** ("marix" ➔ "The Matrix")
*   **Word Order:** ("Batman The" ➔ "The Batman")
*   **Incomplete Titles:** ("man of steel" ➔ "Man of Steel (2013)")

## ⚙️ Tech Stack
*   **Analysis:** Pandas, NumPy, Scikit-Learn
*   **UI:** Streamlit (Web Framework)
*   **Matching:** TheFuzz (Levenshtein distance logic)
*   **Deployment:** Streamlit Cloud / GitHub

## 💻 How to Run Locally
1. Clone the repo: `git clone https://github.com/[YOUR-USERNAME]/movie-recommender.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch: `streamlit run app.py`

## 📬 Contact
Created by **[Waleed Matar]**  
[[LinkedIn](https://www.linkedin.com/in/waleed-matar-392784371/)]

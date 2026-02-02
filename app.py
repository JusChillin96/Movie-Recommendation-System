import streamlit as st
import pandas as pd
from thefuzz import process

# --- 1. SETUP ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System")
st.markdown("Find 10 similar movies based on user behavior and genres!")

# --- 2. LOAD DATA (CACHED & OPTIMIZED) ---
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv")
    df = pd.merge(ratings, movies, on='movieId')
    
    # Calculate stats
    movie_stats = df.groupby('title')['rating'].agg(['mean', 'count'])
    movie_stats.columns = ['average_rating', 'rating_count']
    
    # Filter for popular movies (the ones we will recommend)
    popular_movie_titles = movie_stats[movie_stats['rating_count'] > 50].index
    
    # Create Matrix using ONLY popular movies for speed
    matrix = df.pivot_table(index='userId', columns='title', values='rating')
    popular_matrix = matrix[popular_movie_titles]
    
    # Pre-calculate genres for fast boosting
    genre_dict = df[['title', 'genres']].drop_duplicates().set_index('title')['genres'].to_dict()
    genre_sets = {title: set(genres.split('|')) for title, genres in genre_dict.items()}
    
    all_titles = matrix.columns.tolist()
    
    return popular_matrix, movie_stats, genre_sets, all_titles, df

with st.spinner('Loading movie database...'):
    popular_matrix, movie_stats, genre_sets, all_titles, df = load_data()

# --- 3. THE RECOMMENDATION ENGINE ---
def get_recommendations(user_input, popular_matrix, movie_stats, genre_sets, all_titles, df):
    # 1. Fuzzy Match against ALL movies
    match = process.extractOne(user_input, all_titles, scorer=process.fuzz.token_sort_ratio)
    best_title = match[0]
    score = match[1]
    
    if score < 50:
        return None, f"Could not find a movie close to '{user_input}'."

    # 2. Get ratings for the search movie (even if it's not popular)
    # We grab it from the main dataframe
    target_ratings = df[df['title'] == best_title].pivot_table(index='userId', columns='title', values='rating')[best_title]
    # Reindex to match our popular_matrix users
    target_ratings = target_ratings.reindex(popular_matrix.index)

    # 3. Correlation (Fast)
    similar_to_movie = popular_matrix.corrwith(target_ratings)
    
    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie = corr_movie.join(movie_stats['rating_count'])
    
    # 4. Genre Boost
    selected_genres = genre_sets.get(best_title, set())
    def fast_genre_score(title):
        target_genres = genre_sets.get(title, set())
        return len(selected_genres.intersection(target_genres)) * 0.1

    corr_movie['Final_Score'] = corr_movie['Correlation'] + corr_movie.index.map(fast_genre_score)
    
    # 5. Sort and Filter
    recommendations = corr_movie.sort_values(by='Final_Score', ascending=False)
    
    # Remove the movie itself from results if it's in the popular list
    if best_title in recommendations.index:
        recommendations = recommendations.drop(best_title)
        
    return best_title, recommendations.head(10)

# --- 4. UI ---
user_movie = st.text_input("Enter a Movie Title:", "Man of Steel")

if st.button('Get Recommendations'):
    if user_movie:
        best_title, results = get_recommendations(user_movie, popular_matrix, movie_stats, genre_sets, all_titles, df)
        
        if best_title is None:
            st.error(results)
        elif isinstance(results, str):
            st.warning(results)
        else:
            st.success(f"Best match found: **{best_title}**")
            st.subheader("You might also like:")
            # Only show relevant columns to the user
            st.table(results[['Correlation', 'rating_count']])
    else:
        st.warning("Please enter a movie name.")

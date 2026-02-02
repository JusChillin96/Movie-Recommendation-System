import streamlit as st
import pandas as pd
from thefuzz import process

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System")
st.markdown("Type in a movie you love, and I'll find 10 others just like it based on user ratings!")

# --- 2. LOAD DATA (CACHED) ---
@st.cache_data
def load_data():
    # Load files
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv")
    
    # Merge
    df = pd.merge(ratings, movies, on='movieId')
    
    # Calculate Rating Counts (for filtering)
    movie_stats = df.groupby('title')['rating'].agg(['mean', 'count'])
    movie_stats.columns = ['average_rating', 'rating_count']
    
    # Create Matrix
    matrix = df.pivot_table(index='userId', columns='title', values='rating')
    
    return matrix, movie_stats

# Show a loading spinner while data loads
with st.spinner('Loading the movie database...'):
    matrix, movie_stats = load_data()

# --- 3. THE RECOMMENDATION ENGINE ---
def get_recommendations(user_input, matrix, movie_stats):
    # Get all movie titles
    all_titles = matrix.columns.tolist()
    
    # FUZZY MATCHING: Find the closest title
    match = process.extractOne(user_input, all_titles, scorer=process.fuzz.token_sort_ratio)
    best_title = match[0]
    score = match[1]
    
    # If the match is weak (e.g., < 50%), tell the user
    if score < 50:
        return None, f"Could not find a movie close to '{user_input}'. Did you mean '{best_title}'?"
    
    # Calculate Correlation
    movie_user_ratings = matrix[best_title]
    similar_to_movie = matrix.corrwith(movie_user_ratings)
    
    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie = corr_movie.join(movie_stats['rating_count'])
    
    # Filter: Rating count > 50 and remove the movie itself
    recommendations = corr_movie[corr_movie['rating_count'] > 50].sort_values(by='Correlation', ascending=False)
    
    # Return the top 10 (excluding the first one which is the movie itself)
    return best_title, recommendations.iloc[1:].head(10)

# --- 4. THE USER INTERFACE ---
# Input box
user_movie = st.text_input("Enter a Movie Title:", "The Matrix")

if st.button('Get Recommendations'):
    if user_movie:
        try:
            # Run the logic
            official_title, results = get_recommendations(user_movie, matrix, movie_stats)
            
            if official_title is None:
                st.error(results) # Show error message if no match found
            else:
                st.success(f"Best match found: **{official_title}**")
                st.subheader("You might also like:")
                
                # Display the results as a nice table
                st.table(results[['Correlation', 'rating_count']])
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a movie name.")
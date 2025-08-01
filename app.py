import os
import pickle
import streamlit as st
import requests
import time
import gc
import sys
from requests.exceptions import RequestException

# Memory optimization for Render deployment
if os.environ.get('RENDER') == 'true':
    # Reduce memory usage
    sys.path.append(os.path.dirname(__file__))
    try:
        from model_loader import optimize_movies_file, optimize_neighbors_file
        st.info("Running in Render environment. Optimizing model files for memory efficiency...")
        optimize_movies_file()
        optimize_neighbors_file()
        # Force garbage collection
        gc.collect()
    except Exception as e:
        st.warning(f"Could not optimize model files: {e}")

# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'similar_indices_list' not in st.session_state:
    st.session_state.similar_indices_list = []
if 'selected_movie_index' not in st.session_state:
    st.session_state.selected_movie_index = None
if 'loaded_recommendations' not in st.session_state:
    st.session_state.loaded_recommendations = {'names': [], 'posters': []}

# --- Fetch Poster (cached for speed) ---
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Poster"
    except RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/300x450.png?text=Error"

# --- Load Pickled Files ---
@st.cache_resource(show_spinner=False)
def load_movie_data():
    try:
        # Load only essential columns to reduce memory usage
        movies_df = pickle.load(open('artifacts/movies.pkl', 'rb'))
        
        # Keep only necessary columns
        if 'id' in movies_df.columns and 'title' in movies_df.columns:
            movies_df = movies_df[['id', 'title']].reset_index(drop=True)
        else:
            movies_df = movies_df.reset_index(drop=True)
            
        return movies_df
    except FileNotFoundError:
        st.error("Movies data file not found. Please make sure 'artifacts/movies.pkl' exists.")
        st.stop()
        return None

@st.cache_resource(show_spinner=False)
def load_similarity_indices():
    try:
        return pickle.load(open('artifacts/all_neighbors.pkl', 'rb'))
    except FileNotFoundError:
        st.error("Similarity indices file not found. Please make sure 'artifacts/all_neighbors.pkl' exists.")
        st.stop()
        return None

# Load data with memory optimization
movies = load_movie_data()
similar_indices = load_similarity_indices()

# --- Get Similar Movie Indices ---
def get_similar_indices(movie):
    if movie not in movies['title'].values:
        return []
    
    # Use memory-efficient approach
    index = movies[movies['title'] == movie].index[0]
    
    # Get only the first 30 similar movies to reduce memory usage
    # We'll limit to 30 since most users won't scroll through more than 30 recommendations
    return similar_indices[index][1:31]

# --- Load Batch of Recommendations ---
def load_recommendations_batch(indices, start_idx, batch_size=5):
    """Load a batch of movie recommendations with memory optimization"""
    # Reduce batch size to 5 to minimize memory usage
    end_idx = min(start_idx + batch_size, len(indices))
    names = []
    posters = []
    
    # Show a progress bar while loading
    progress_bar = st.progress(0)
    
    for i, movie_idx in enumerate(indices[start_idx:end_idx]):
        # Get movie details one at a time to reduce memory usage
        movie_id = movies.iloc[movie_idx]['id']
        names.append(movies.iloc[movie_idx]['title'])
        
        # Fetch poster with error handling to prevent crashes
        try:
            poster = fetch_poster(movie_id)
            posters.append(poster)
        except Exception as e:
            st.warning(f"Could not load poster for {movies.iloc[movie_idx]['title']}")
            posters.append("https://via.placeholder.com/300x450.png?text=No+Poster")
        
        # Update progress bar
        progress = (i + 1) / (end_idx - start_idx)
        progress_bar.progress(progress)
        
        # Add a small delay to prevent memory spikes
        time.sleep(0.1)
        
    # Remove progress bar when done
    progress_bar.empty()
    
    return names, posters, end_idx

# --- Memory-Optimized Streamlit UI ---
st.markdown("<h1 style='text-align: center; color: red;'>CineML: Movie Recommender</h1>", unsafe_allow_html=True)

# Use a container to better manage memory
with st.container():
    # Create a search box with autocomplete
    movie_options = movies['title'].tolist()
    selected_movie = st.selectbox(
        "Type or Select a movie to get recommendations",
        options=movie_options,
        index=0 if movie_options else None
    )
    
    # Reset pagination when a new movie is selected
    if st.session_state.selected_movie_index is None or st.session_state.selected_movie_index != selected_movie:
        st.session_state.page = 1
        st.session_state.loaded_recommendations = {'names': [], 'posters': []}
        # Clear memory
        import gc
        gc.collect()

# Use a separate container for recommendations to manage memory better
with st.container():
    if st.button('Show Recommendations', key='show_rec_button'):
        # Reset previous recommendations
        st.session_state.loaded_recommendations = {'names': [], 'posters': []}
        st.session_state.page = 1
        
        # Get similar movie indices (limited to 30 for memory efficiency)
        st.session_state.similar_indices_list = get_similar_indices(selected_movie)
        st.session_state.selected_movie_index = selected_movie
        
        if len(st.session_state.similar_indices_list) > 0:
            # Load first batch of recommendations (reduced batch size)
            with st.spinner('Loading recommendations...'):
                names, posters, _ = load_recommendations_batch(
                    st.session_state.similar_indices_list, 
                    0, 
                    batch_size=5  # Reduced batch size
                )
                
                st.session_state.loaded_recommendations['names'] = names
                st.session_state.loaded_recommendations['posters'] = posters
        else:
            st.error(f"No recommendations found for {selected_movie}")
            
        # Force garbage collection
        import gc
        gc.collect()

# Display loaded recommendations in a memory-efficient way
if len(st.session_state.loaded_recommendations['names']) > 0:
    with st.container():
        st.subheader(f"Recommendations for '{st.session_state.selected_movie_index}'")
        
        # Display in a grid (3 movies per row instead of 5 to reduce memory usage)
        total = len(st.session_state.loaded_recommendations['names'])
        rows = (total + 2) // 3  # Changed from 5 to 3 columns
        
        for row in range(rows):
            cols = st.columns(3)  # Changed from 5 to 3 columns
            for i in range(3):    # Changed from 5 to 3 columns
                idx = row * 3 + i  # Changed from 5 to 3 columns
                if idx < total:
                    with cols[i]:
                        st.text(st.session_state.loaded_recommendations['names'][idx])
                        # Use a smaller image size to reduce memory
                        st.image(st.session_state.loaded_recommendations['posters'][idx], width=200)
    
    # Load more button - only if we have less than 15 recommendations loaded
    # This limits total recommendations to save memory
    current_loaded = len(st.session_state.loaded_recommendations['names'])
    similar_indices_length = len(st.session_state.similar_indices_list)
    
    if current_loaded < similar_indices_length and current_loaded < 15:
        with st.container():
            if st.button("Load More Recommendations", key='load_more_button'):
                # Load next batch with reduced batch size
                with st.spinner('Loading more recommendations...'):
                    names, posters, _ = load_recommendations_batch(
                        st.session_state.similar_indices_list,
                        current_loaded,
                        batch_size=5  # Reduced batch size
                    )
                    
                    # Append to existing recommendations
                    st.session_state.loaded_recommendations['names'].extend(names)
                    st.session_state.loaded_recommendations['posters'].extend(posters)
                    
                    # Force garbage collection
                    import gc
                    gc.collect()
                    
                    # Force a rerun to display the new recommendations
                    st.rerun()
    
    # Add a note about memory optimization
    st.caption("Note: Showing a limited number of recommendations to optimize performance.")

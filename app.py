import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'similar_indices_list' not in st.session_state:
    st.session_state.similar_indices_list = []
if 'selected_movie_index' not in st.session_state:
    st.session_state.selected_movie_index = None
if 'loaded_recommendations' not in st.session_state:
    st.session_state.loaded_recommendations = {'names': [], 'posters': []}

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    session = requests.Session()
    retry_strategy = Retry(
        total=1,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY')}&language=en-US"
    
    try:
        response = session.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w300{poster_path}"
    except:
        pass
    
    return f"https://via.placeholder.com/300x450/FF6B6B/FFFFFF?text=Movie+{movie_id}"

# --- Load Pickled Files ---
try:
    movies = pickle.load(open('artifacts/movies.pkl', 'rb')).reset_index(drop=True)
    similar_indices = pickle.load(open('artifacts/all_neighbors.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please make sure the 'artifacts' directory contains the required model files.")
    st.stop()

# --- Get Similar Movie Indices ---
def get_similar_indices(movie):
    if movie not in movies['title'].values:
        return []
    
    index = movies[movies['title'] == movie].index[0]
    # Get up to 100 similar movies (excluding the selected movie itself)
    return similar_indices[index][1:101]

# --- Load Batch of Recommendations ---
def load_recommendations_batch(indices, start_idx, batch_size=10):
    """Load a batch of movie recommendations"""
    end_idx = min(start_idx + batch_size, len(indices))
    names = []
    posters = []
    
    # Show a progress bar while loading
    progress_bar = st.progress(0)
    
    for i, movie_idx in enumerate(indices[start_idx:end_idx]):
        movie_id = movies.iloc[movie_idx]['id']
        names.append(movies.iloc[movie_idx]['title'])
        posters.append(fetch_poster(movie_id))
        
        # Update progress bar
        progress = (i + 1) / (end_idx - start_idx)
        progress_bar.progress(progress)
        
    # Remove progress bar when done
    progress_bar.empty()
    
    return names, posters, end_idx

# --- Streamlit UI ---
st.markdown("<h1 style='text-align: center; color: red;'>CineML: Movie Recommender</h1>", unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or Select a movie to get recommendations", movie_list)

# Reset pagination when a new movie is selected
if st.session_state.selected_movie_index is None or st.session_state.selected_movie_index != selected_movie:
    st.session_state.page = 1
    st.session_state.loaded_recommendations = {'names': [], 'posters': []}

if st.button('Show Recommendations'):
    # Reset previous recommendations
    st.session_state.loaded_recommendations = {'names': [], 'posters': []}
    st.session_state.page = 1
    
    # Get similar movie indices
    st.session_state.similar_indices_list = get_similar_indices(selected_movie)
    st.session_state.selected_movie_index = selected_movie
    
    if len(st.session_state.similar_indices_list) > 0:
        # Load first batch of recommendations
        names, posters, _ = load_recommendations_batch(
            st.session_state.similar_indices_list, 
            0, 
            batch_size=10
        )
        
        st.session_state.loaded_recommendations['names'] = names
        st.session_state.loaded_recommendations['posters'] = posters
    else:
        st.error(f"No recommendations found for {selected_movie}")

# Display loaded recommendations
if len(st.session_state.loaded_recommendations['names']) > 0:
    st.subheader(f"Recommendations for '{st.session_state.selected_movie_index}'")
    
    # Display in a grid (5 movies per row)
    total = len(st.session_state.loaded_recommendations['names'])
    rows = (total + 4) // 5
    
    for row in range(rows):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            if idx < total:
                with cols[i]:
                    st.text(st.session_state.loaded_recommendations['names'][idx])
                    st.image(st.session_state.loaded_recommendations['posters'][idx])
    
    # Load more button
    current_loaded = len(st.session_state.loaded_recommendations['names'])
    similar_indices_length = len(st.session_state.similar_indices_list)
    if current_loaded < similar_indices_length:
        if st.button("Load More Recommendations"):
            # Load next batch
            names, posters, _ = load_recommendations_batch(
                st.session_state.similar_indices_list,
                current_loaded,
                batch_size=10
            )
            
            # Append to existing recommendations
            st.session_state.loaded_recommendations['names'].extend(names)
            st.session_state.loaded_recommendations['posters'].extend(posters)
            
            # Force a rerun to display the new recommendations
            st.rerun()

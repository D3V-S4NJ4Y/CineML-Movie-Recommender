import os
import pickle
import streamlit as st
import requests
from requests.exceptions import RequestException

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
movies = pickle.load(open('artifacts/movies.pkl', 'rb')).reset_index(drop=True)
similar_indices = pickle.load(open('artifacts/all_neighbors.pkl', 'rb'))

# --- Recommend Function ---
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    
    index = movies[movies['title'] == movie].index[0]
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in similar_indices[index][1:101]:  # 100 recommendations (skip the selected movie itself)
        movie_id = movies.iloc[i]['id']
        recommended_movies_name.append(movies.iloc[i]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies_name, recommended_movies_poster

# --- Streamlit UI ---
st.markdown("<h1 style='text-align: center; color: red;'>CineML: Movie Recommender</h1>", unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or Select a movie to get recommendations", movie_list)

if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    total = len(recommended_movies_name)
    rows = (total + 4) // 5  # 5 movies per row

    for row in range(rows):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            if idx < total:
                with cols[i]:
                    st.text(recommended_movies_name[idx])
                    st.image(recommended_movies_poster[idx])

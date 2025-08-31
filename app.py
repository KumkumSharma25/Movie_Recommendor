import streamlit as st
import pickle
import requests
import pandas as pd

# Function to fetch poster safely
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b6851b0ab4506d1d76a192319876c66c&language=en-US"
    data = requests.get(url).json()
    
    poster_path = data.get('poster_path')  # use .get() to avoid KeyError
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Placeholder if poster is missing
        full_path = "https://via.placeholder.com/500x750?text=No+Image"
    
    return full_path

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Correct movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("Movie Recommender System 🎬")

selected_movie = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5)
    
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)

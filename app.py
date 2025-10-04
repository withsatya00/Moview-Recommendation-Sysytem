import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=674443df2a448329f965c28707fbb2f6&language=en-US"
    data = requests.get(url).json()
    if "poster_path" in data and data["poster_path"]:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters


# -------- Streamlit UI ---------
st.title("🎬 Movie Recommendation System")

# load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # 5 posters per row
    # 5 posters per row
    for i in range(0, len(names), 5):
        cols = st.columns(5)
        for col, name, poster in zip(cols, names[i:i+5], posters[i:i+5]):
            with col:
                st.image(poster, use_container_width=True)   # changed parameter
                st.caption(name)                             # movie name below


import streamlit as st
import pickle
import pandas as pd
import requests

st.title("Movie Recommended System")
movies_lis = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_lis)
# # movies_list = movies_list['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))

movies_list = movies['title'].values
selected_movie_name = st.selectbox('Type or Select a movie from the dropdown',movies_list)


def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9936bd8062d008119565c9245507fd8c'.format(movie_id))
    #data = requests.get(response)
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']
    

def recommend(movie):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse = True,key=lambda x:x[1])[1:6]
    
    recommended_movie = []
    recommended_movie_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movie.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie,recommended_movie_posters


if st.button("Show Recommend"):
    recommended_movie,recommended_movie_posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_movie[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie[1])
        st.image(recommended_movie_posters[1])
    with col1:
        st.text(recommended_movie[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie[4])
        st.image(recommended_movie_posters[4])

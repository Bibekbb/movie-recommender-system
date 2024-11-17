import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500"
    except Exception as e:
        return "https://via.placeholder.com/500"

try:
    df = pickle.load(open("model/movies_recommended.pkl", 'rb'))
    cs = pickle.load(open("model/cs.pkl", 'rb'))
    movies_list = df['title'].values
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

st.header("Movie Recommender System")

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

example_image_ids = [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]
image_urls = [fetch_poster(movie_id) for movie_id in example_image_ids]
imageCarouselComponent(imageUrls=image_urls, height=200)

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    similarity_scores = sorted(enumerate(cs[movie_index]), key=lambda x: x[1], reverse=True)
    
    recommended_movies, recommended_posters = [], []
    for i in similarity_scores[1:6]: 
        movie_id = df.iloc[i[0]].id
        recommended_movies.append(df.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

with st.form("movie_form"):
    selected_movie = st.selectbox("Select a movie", movies_list)
    recommend_button = st.form_submit_button("Recommend")

if recommend_button:
    movie_names, movie_posters = recommend(selected_movie)
    
    columns = st.columns(5)
    for col, name, poster in zip(columns, movie_names, movie_posters):
        with col:
            st.text(name)
            st.image(poster)

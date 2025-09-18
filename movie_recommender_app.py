import streamlit as st
import pickle
from huggingface_hub import hf_hub_download

# Recommend function to load the recommended movies list
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
    return recommended_movies

# Loading the pickle data
movies = pickle.load(open('movies.pkl', 'rb'))
HF_REPO_ID = "Chanduyemul/movie-similarity"
FILENAME = "similarity.pkl"

@st.cache_data(show_spinner=False)
def load_similarity():
    local_path = hf_hub_download(repo_id=HF_REPO_ID, filename=FILENAME, repo_type="dataset")
    with open(local_path, "rb") as f:
        sim = pickle.load(f)
    return sim

similarity = load_similarity()

# Title
st.markdown(
    "<h1 style='text-align:center; color:#FF4B4B;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

# Selection of a movie
selected_movie_name = st.selectbox(
    "📌 Select a movie to get recommendations:",
    movies['title'].values
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    find_btn = st.button("✨ Find Recommendations", type="primary")

# Recommendation button
if find_btn:
    recommendations= recommend(selected_movie_name)

    st.markdown("### 🎥 Recommended Movies")

    cols=st.columns(2)
    for idx,movie in enumerate(recommendations,start=1):
        col = cols[(idx - 1) % 2] # this distributes the names into 2 columns
        with col:
            st.markdown(
                f"""
                <div style="
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 10px 14px;
                    margin: 8px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
                ">
                    <h5 style="margin:0; color:#333; font-size:16px; font-weight:500;">
                        {idx}. {movie}
                    </h5>
                </div>
                """,
                unsafe_allow_html=True
            )
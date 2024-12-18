import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "8610581150584025b80bc52ffd8c8f8d"
CLIENT_SECRET = "e49a91ea2b1c4480b91439739dc81065"

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load music dataset and similarity matrix
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch album cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    return "https://i.postimg.cc/0QNxYz4V/social.png"  # Fallback image

# Recommendation function
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:9]:  # Top 8 recommendations
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

# Streamlit App
#st.title("Spotify Music Recommender")
# Center-align the title
st.markdown("""
    <div style="text-align: center; font-size: 2.5rem; font-weight: bold; color: #1db954; margin-bottom: 20px;">
        MUSIC RECOMMENDER SYSTEM
    </div>
""", unsafe_allow_html=True)

#st.set_page_config(page_title="Music Recommender System", page_icon="🎵", layout="wide")
st.markdown("""
    <style>
    /* Apply the background image to the entire app */
    html, body, [data-testid="stAppViewContainer"] {
        background-image: url('https://wallpaperaccess.com/full/1373278.jpg'); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        height: 100%;
        width: 100%;
        margin: 0; /* Remove default margin */
        padding: 0; /* Remove default padding */
    }

    /* Optional: Add a dark overlay to improve readability */
    html::before, body::before, [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Black overlay with 50% transparency */
        z-index: -1; /* Push behind content */
    }

    /* Style adjustments to ensure text stands out */
    h1, h2, h3, h4, h5, h6, p, div {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Add shadow for better contrast */
    }

    /* Optional: Center-align title for a polished look */
    .css-10trblm.e16nr0p33 { /* Adjusts the default Streamlit header area */
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

st.header('🎵 Discover Your Next Favorite Song!')

# Dropdown for song selection
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list,
    key="song_selector"
)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    cols = st.columns(8)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_music_posters[idx], use_container_width=True)
            st.caption(recommended_music_names[idx])

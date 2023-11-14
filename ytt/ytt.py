import re
import requests
import threading
import yt_dlp
import assemblyai as aai
import streamlit as st
from configure import AUTH_KEY

# Constants
CHUNK_SIZE = 5242880  # 5MB
YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    'ffmpeg-location': './',
    'outtmpl': "./%(id)s.%(ext)s",
}
HEADERS_AUTH_ONLY = {'authorization': AUTH_KEY}
HEADERS = {"authorization": AUTH_KEY, "content-type": "application/json"}
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
YOUTUBE_PATTERN = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'

# Initialize session state
if 'status' not in st.session_state:
    st.session_state['status'] = 'submitted'
if 'show_transcript' not in st.session_state:
    st.session_state['show_transcript'] = False

# Helper functions
def get_vid(_id):
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        return ydl.extract_info(_id)

def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data

def is_youtube_link(link):
    return bool(re.match(YOUTUBE_PATTERN, link))

def get_id(link):
    _id = link.split('=')[1]
    if '&' in _id:
        _id = _id.split('&')[0]
    return _id

# Streamlit functions
@st.cache_data
def get_audio(link):
    _id = get_id(link)
    meta = get_vid(_id)
    save_location = meta['id'] + '.mp3'
    return save_location

@st.cache_data
def transcribe(link, categories):
    save_location = get_audio(link)
    upload_response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS_AUTH_ONLY, data=read_file(save_location))
    audio_url = upload_response.json()['upload_url']
    transcript_request = {"audio_url": audio_url, "iab_categories": 'True' if categories else 'False'}
    transcript_response = requests.post(TRANSCRIPT_ENDPOINT, json=transcript_request, headers=HEADERS)
    transcript_id = transcript_response.json()['id']
    poll_endpoint = TRANSCRIPT_ENDPOINT + '/' + transcript_id
    return poll_endpoint

@st.cache_data
def get_subtitles(link):
    aai.settings.api_key = AUTH_KEY
    audio_location = get_audio(link)

    text = aai.Transcriber().transcribe(audio_location)
    subtitles = text.export_subtitles_srt()

    #save subtitle to file, file name is youtube video id
    
    #get video id
    _id = get_id(link)

    meta = get_vid(_id)
    save_location = meta['id'] + '.srt'

    f = open(save_location, "a")
    f.write(subtitles)
    f.close()

    print("Saved subtitle to " + save_location)
    
    return save_location

@st.cache_data
def subtitle_to_lyrics(subtitle):
    with open(subtitle, 'r') as srt_file:
        srt_contents = srt_file.read()
    lyrics = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', srt_contents)
    with open('lyrics.txt', 'w') as txt_file:
        txt_file.write(lyrics)
    return lyrics

def get_status(polling_endpoint):
    polling_response = requests.get(polling_endpoint, headers=HEADERS)
    st.session_state["status"] = polling_response.json()["status"]

def refresh_state():
    st.session_state["status"] = "submitted"

# Streamlit UI
st.title("Youtube Transcriber")
link = st.text_input("Enter YouTube link",  on_change=refresh_state)

if link == '':
    st.text("Please enter a link")
    st.stop()

if not is_youtube_link(link):
    st.text("Please enter a YouTube link")
    st.stop() 

st.video(link)
st.text("The transcription is " + st.session_state['status'])

poll_endpoint = transcribe(link,False)
subs = get_subtitles(link)
vid_id = get_id(link)
file_name = vid_id + '.srt'

col1, col2 = st.columns([1, 1])
with col1:
    st.button("Check Status", on_click=get_status, args=(poll_endpoint,))
with col2:
    st.download_button(
    label="Download Subtitles",
    data= subs,
    file_name=file_name,
    mime="text/srt",
) 

if st.session_state['status'] == 'completed':
    poll_endpoint = requests.get(poll_endpoint, headers=HEADERS)
    transcript = poll_endpoint.json()['text']
    formatted_transcript = '\n'.join(transcript.split('. '))
    
col3, col4 = st.columns([1, 1])
with col3:
    st.download_button(
    label="Download Lyrics",
    data=subtitle_to_lyrics(subs),
    file_name='lyrics.txt',
    mime="text/plain",
)
with col4:
    if st.button("Toggle Transcript"):
        st.session_state['show_transcript'] = not st.session_state['show_transcript']

    if st.session_state['show_transcript']:
        st.text_area("Transcript", value=formatted_transcript, height=500)





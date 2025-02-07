import streamlit as st
import whisper
import os
import tempfile
from pydub import AudioSegment
# from openai import OpenAI

# Initialize Whisper model
model = whisper.load_model("base")

# Function to convert audio to WAV (if needed)
def convert_to_wav(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio = AudioSegment.from_file(audio_file)
        audio.export(temp_wav.name, format="wav")
        return temp_wav.name

# Function to transcribe audio with timestamps
def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, word_timestamps=True)
    transcript = []
    for segment in result["segments"]:
        transcript.append((segment["start"], segment["text"]))
    return transcript

# Function to search keywords in transcript
def search_transcript(transcript, keyword):
    results = [segment for segment in transcript if keyword.lower() in segment[1].lower()]
    return results

# Streamlit UI
st.title("🎙️ Podcast Search & Indexing Tool")
st.write("Upload a podcast, transcribe it, and search by keywords!")

uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/mp3')
    
    # Convert to WAV if necessary
    with st.spinner("Processing audio..."):
        audio_path = convert_to_wav(uploaded_file)
        transcript = transcribe_audio(audio_path)
    
    st.subheader("📝 Full Transcription")
    for timestamp, text in transcript:
        st.write(f"[{timestamp:.2f}s]: {text}")
    
    # Keyword search functionality
    search_query = st.text_input("🔍 Search in transcript")
    if search_query:
        results = search_transcript(transcript, search_query)
        if results:
            st.subheader("🔎 Search Results")
            for timestamp, text in results:
                st.write(f"[{timestamp:.2f}s]: {text}")
        else:
            st.warning("No matches found!")
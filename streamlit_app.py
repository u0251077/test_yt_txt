import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Sidebar for API key and model selection
st.sidebar.header("Google API Configuration")
google_api_key = st.sidebar.text_input("Google API Key", key="google_api_key", type="password")
selected_model = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])

st.title("YouTube Transcript Summarizer")

# Input URL and button to generate summary
youtube_url = st.text_input("Enter YouTube URL")
if st.button("Generate Summary"):
    if not youtube_url:
        st.error("Please enter a YouTube URL.")
    else:
        # Extract video ID from URL
        match = re.search(r"(?<=youtu\.be/)[\w-]+", youtube_url)
        if match:
            video_id = match.group(0)
            try:
                # Get transcript
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-TW', 'zh-Hans'])
                
                # Combine transcript into a single string
                full_text = ' '.join(item['text'] for item in transcript)
                
                # Display transcript
                st.text_area("Transcript", value=full_text, height=300, max_chars=None)
                
                if google_api_key:
                    # Configure Google API key
                    genai.configure(api_key=google_api_key)
                    
                    # Generate summary
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(full_text)
                    
                    # Display summary
                    summary = '請使用中文,協助我將以上內容進行摘要,內容為:' + response.text  # Adjust this if the response format differs
                    st.text_area("Summary", value=summary, height=300, max_chars=None)
                else:
                    st.error("Please enter your Google API key in the sidebar.")
            except Exception as e:
                st.error(f"Error fetching transcript: {e}")
        else:
            st.error("Invalid YouTube URL.")

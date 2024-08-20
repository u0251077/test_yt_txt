import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Sidebar for API key and model selection
st.sidebar.header("Google API Configuration")
google_api_key = st.sidebar.text_input("Google API Key", key="google_api_key", type="password")
selected_model = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
"[Get an Gemini API key](https://ai.google.dev/gemini-api?hl=zh-tw)"


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
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh', 'en', 'zh-TW', 'zh-Hans', 'zh-Hant'])
                # Combine transcript into a single string
                full_text = ' '.join(item['text'] for item in transcript)
                #st.write("Transcript:") #輸出完整文字內容
                #st.text_area(full_text)
                
                if google_api_key:
                    # Configure Google API key
                    genai.configure(api_key=google_api_key)
                    
                    # Generate summary with custom prompt
                    model = genai.GenerativeModel(selected_model)
                    prompt = f"請用繁體中文協助我將以下內容進行摘要分析：\n\n{full_text}"
                    response = model.generate_content(prompt)
                    
                    # Display summary
                    summary = response.text  # Adjust this if the response format differs
                    
                    message = st.chat_message("assistant")
                    message.write("Summary")
                    message.write(summary)
                    
                else:
                    st.error("Please enter your Google API key in the sidebar.")
            except Exception as e:
                st.error(f"Error fetching transcript: {e}")
        else:
            st.error("Invalid YouTube URL.")

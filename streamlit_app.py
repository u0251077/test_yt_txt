import streamlit as st
from pytube import YouTube
import whisper
import openai
import os

# OpenAI API 金鑰
openai.api_key = 'your-api-key'

st.title('YouTube 影片轉文字並生成摘要')

# 輸入 YouTube 影片 URL
video_url = st.text_input('請輸入 YouTube 影片 URL:')

if video_url:
    # 步驟 1：使用 pytube 下載 YouTube 影片音訊
    st.write("下載音訊中...")
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(filename="audio.mp4")

    st.write("音訊下載完成。")

    # 步驟 2：使用 Whisper 將音訊轉換為文字
    st.write("轉換音訊為文字中...")
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp4")
    text = result['text']
    st.write("轉換完成。")

    # 顯示轉換出的文字
    st.subheader('影片文字內容:')
    st.text_area("影片內容:", text, height=200)

    # 步驟 3：使用 OpenAI API 生成摘要
    st.write("生成摘要中...")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"請總結以下影片內容：\n\n{text}"}
        ]
    )

    summary = response['choices'][0]['message']['content']
    st.subheader('影片摘要:')
    st.write(summary)

    # 清理音訊檔案
    os.remove("audio.mp4")

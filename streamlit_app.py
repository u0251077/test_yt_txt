import streamlit as st
import openai
from tempfile import NamedTemporaryFile
from openai import OpenAI


# 設置你的 API 金鑰
api_key = st.text_input('請輸入 OpenAI API 金鑰', type='password')
openai.api_key = api_key
client = OpenAI(api_key=api_key)
st.title('音訊轉錄並生成摘要')

# 上傳音訊文件
uploaded_file = st.file_uploader("上傳音訊檔案", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file and api_key:
    # 保存上傳的文件到臨時文件
    with NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    audio_file= open(temp_file_path, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )
    st.write(transcription.text)

    
    # 顯示轉錄結果
    transcription_text = response['text']
    st.subheader('音訊轉錄內容:')
    st.text_area("音訊內容:", transcription_text, height=200)

    # 清理臨時文件
    os.remove(temp_file_path)
else:
    st.warning("請輸入 OpenAI API 金鑰並上傳音訊檔案。")

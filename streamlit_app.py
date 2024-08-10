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

# 对话函数
def chat_with_gpt(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "請用中文摘要以下內容"+prompt}
        ],
        max_tokens=150
    )
    return completion.choices[0].message.content.strip()


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
    st.success(chat_with_gpt(transcription.text), icon="✅")

    
    # 清理臨時文件
    os.remove(temp_file_path)
else:
    st.warning("請輸入 OpenAI API 金鑰並上傳音訊檔案。")

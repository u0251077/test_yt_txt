import streamlit as st
import whisper
import openai
import os
from tempfile import NamedTemporaryFile

# OpenAI API 金鑰
openai.api_key = 'your-api-key'

st.title('影片轉文字並生成摘要')

# 上傳影片
uploaded_file = st.file_uploader("上傳影片檔案", type=["mp4", "m4a", "wav", "flac"])

if uploaded_file is not None:
    # 將上傳的文件保存到臨時文件中，並添加適當的擴展名
    suffix = os.path.splitext(uploaded_file.name)[1]  # 獲取原文件的擴展名
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    st.write(f"影片上傳完成，文件路徑：{temp_file_path}")

    # 使用 Whisper 將音訊轉換為文字
    st.write("轉換音訊為文字中...")
    model = whisper.load_model("base")
    result = model.transcribe(temp_file_path)
    text = result['text']
    st.write("轉換完成。")

    # 顯示轉換出的文字
    st.subheader('影片文字內容:')
    st.text_area("影片內容:", text, height=200)

    # 使用 OpenAI API 生成摘要
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

    # 清理臨時文件
    os.remove(temp_file_path)

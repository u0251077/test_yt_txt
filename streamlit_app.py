import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Streamlit应用程序
st.title('YouTube 字幕提取器')

# 输入URL
url = st.text_input('请输入YouTube视频URL', 'https://youtu.be/EHpzHtP1FpE')

# 提取视频ID
def extract_video_id(url):
    match = re.search(r"(?<=youtu\.be/)[\w-]+", url)
    return match.group(0) if match else None

if url:
    video_id = extract_video_id(url)
    
    if video_id:
        st.write(f"提取的视频ID: {video_id}")

        try:
            # 获取字幕
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-TW', 'zh-Hans'])
            
            # 将字幕内容组合成一整串的文字
            full_text = ' '.join(item['text'] for item in transcript)
            
            # 显示组合后的文本内容
            st.text_area('提取的字幕内容', full_text, height=300)
        except Exception as e:
            st.error(f"无法获取字幕：{e}")
    else:
        st.error("无法提取视频ID")

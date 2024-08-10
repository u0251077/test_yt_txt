import streamlit as st
from pytube import YouTube

# 标题
st.title("YouTube 视频下载器")

# 输入框获取 YouTube 视频链接
video_url = st.text_input("输入 YouTube 视频链接:")

if video_url:
    try:
        yt = YouTube(video_url)
        st.write(f"视频标题: {yt.title}")
        st.write(f"视频时长: {yt.length} 秒")
        
        # 选择下载的分辨率
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
        stream_options = {f"{stream.resolution} - {stream.fps}fps": stream for stream in streams}
        selected_stream = st.selectbox("选择分辨率:", list(stream_options.keys()))
        
        # 下载按钮
        if st.button("下载视频"):
            stream = stream_options[selected_stream]
            stream.download()
            st.success("视频下载成功!")
    except Exception as e:
        st.error(f"下载视频时出错: {e}")

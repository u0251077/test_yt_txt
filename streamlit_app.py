import streamlit as st
import yt_dlp

# 标题
st.title("YouTube 视频下载器")

# 输入框获取 YouTube 视频链接
video_url = st.text_input("输入 YouTube 视频链接:")

# 文件保存路径
download_path = st.text_input("输入保存路径 (默认为当前目录):", value=".")

if video_url:
    try:
        # 显示可用的格式选项
        ydl_opts = {'quiet': True, 'skip_download': True, 'listformats': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])
            format_options = [f"{fmt['format_id']} - {fmt['format_note']} - {fmt['ext']}" for fmt in formats]
        
        # 选择格式
        selected_format = st.selectbox("选择格式:", format_options)
        format_id = selected_format.split(" ")[0]

        # 下载按钮
        if st.button("下载视频"):
            ydl_opts = {
                'format': format_id,
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            st.success("视频下载成功!")
    except Exception as e:
        st.error(f"下载视频时出错: {e}")

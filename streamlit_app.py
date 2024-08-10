import streamlit as st
import subprocess
import os

# 标题
st.title("YouTube 视频下载器")

# 输入框获取 YouTube 视频链接
video_url = st.text_input("输入 YouTube 视频链接:")

# 文件保存路径
download_path = st.text_input("输入保存路径 (默认为当前目录):", value=".")

if video_url:
    try:
        # 下载选项
        if st.button("下载视频"):
            # 使用 youtube-dl 命令行工具下载视频
            cmd = f'youtube-dl -o "{download_path}/%(title)s.%(ext)s" {video_url}'
            process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if process.returncode == 0:
                st.success("视频下载成功!")
            else:
                st.error(f"下载失败: {process.stderr.decode('utf-8')}")
    except Exception as e:
        st.error(f"下载视频时出错: {e}")

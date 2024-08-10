import yt_dlp as youtube_dl

def download_audio_from_youtube(url, output_audio_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_audio_path
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    st.write(f"Audio downloaded and saved to {output_audio_path}")


# 示例使用
youtube_url = "https://youtu.be/gOCN-mU7qkg"  
output_audio_path = "downloaded_audio"

# 下载 YouTube 音频
st.write("test")
#download_audio_from_youtube(youtube_url, output_audio_path)


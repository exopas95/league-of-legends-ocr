import src.constants as constants
from pytube import YouTube

def download_video_and_title(video_url):    
    # Download youtube video
    print("Start downloading...")
    try:
        yt = YouTube(video_url)
        yt.streams.filter(file_extension='mp4', resolution='1080p')[0].download(constants.VIDEO_PATH)
    except Exception as e:
        print('video_download_error',  e)
    print("Downloading finished...")

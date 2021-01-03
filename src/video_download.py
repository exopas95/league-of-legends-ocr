import src.constants as constants
from pytube import YouTube

def download_video_and_title():    

    # Get youtube link list from text file
    f = open("youtube_list.txt", "r")
    youtube_url_list = f.read().splitlines()
    print("Reading youtube link from the youtube_list.txt file")
    f.close()

    # Download youtube video
    print("Start downloading...")
    for video_url in youtube_url_list:
        print(video_url)
        try:
            yt = YouTube(video_url)
            print(f"Start downloading from {video_url}")
            yt.streams.filter(file_extension='mp4', resolution='1080p')[0].download(constants.VIDEO_PATH)
        except Exception as e:
            print('video_download_error',  e)
    print("Downloading finished...")

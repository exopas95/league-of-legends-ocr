import os
import src.convert_ocr as convert_ocr
import src.video_download as video_download
import src.constants as constants
from multiprocessing import Pool

if __name__ == "__main__":
    f = open("youtube_list.txt", "r")
    youtube_url_list = f.read().splitlines()
    f.close()

    pool = Pool(processes=2)

    i_url=0
    isAllDownloadDone = False
    while True :
        video_list = os.listdir(constants.VIDEO_PATH)
        if len(video_list) < 2 :
            if i_url < len(youtube_url_list) :
                video_download.download_video_and_title(youtube_url_list[i_url])
                i_url += 1
            else :
                isAllDownloadDone = True
        else :
            pool.map(convert_ocr.run, video_list)

        if (isAllDownloadDone) & (len(video_list)==0) :
            break;
            

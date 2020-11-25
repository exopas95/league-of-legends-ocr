import sys
import src.convert_ocr as convert_ocr
import src.video_download as video_download


if __name__ == "__main__":
    print("\n")
    print("#-------------------------------------------#")
    print("#   1. Download Youtube Video               #")
    print("#   2. Process OCR from the youtube video   #")
    print("#-------------------------------------------#")
    print("Input a number and press enter to process: ", end='')
    num = int(sys.stdin.readline())
    print("\n")

    while True:
        if num == 1:
            video_download.download_video_and_title()
            break
        elif num == 2:
            convert_ocr.run()
            break
        else:
            print("Please type a number from the menu: ", end="")
            num = int(sys.stdin.readline())
            

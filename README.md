# opgg-ocr
OP.GG

## Introduction
This repository contains code for Optical Character Recognition on League of Legends game video.
The purpose of this project is as follows:
- Extract meaningful text values such as gold, level, KDA from League of Legends game video using GCP OCR API
- Develop various scenarios on what analysis can be done based on the extracted values.

## Dependencies
The code is compatible with python3 and the following dependencies are needed to run the program.
- `pandas == 1.1.5`
- `google-cloud-videointelligence == 1.16.0`
- `opencv-python == 4.2.0.34`
- `google-cloud-vision == 2.0.0`
- `pillow == 8.0.1`
- `tqdm == 4.51.0`
- `pytube == 10.0.0`

Please use the command below to install all the dependencies.<br>
``` !pip install -r requirements.txt --use-feature=2020-resolver ```

## Installation
1. Clone the repository:
``` https://github.com/nwojke/deep_sort.git ```

2. Create credential.json file from GCP 
    If you are a member of the project, please create the credential file from OPGG service account
    - you can create the file from GCP - IAM & ADMIN - Service Accounts - Actions - Create Key<br>

    If you are not a member of the project, please create your credential file 
    according to the instruction of Google Cloud Vision API<br>

    After your done with creating credential file, please loacte the file in the same path as the run.py file

## Modify Path
Please modify the following path of the constnats.py file that matches your OS.
- `VIDEO_PATH`
- `IMAGE_PATH`
- `CSV_PATH`

## Download Game Video from Youtube
First, modify youtube_list.txt file and add the url you want to download <br>
Run the program by using the following command and press 1
``` python run.py ```

## Generating OCR Tracker
Run the program by using the following command and press 2
``` python run.py ```

## Highlevel overview of source files
In package `conver_ocr.py` is the main tracking code:
- `bitwise_operation.py`: bitwise operation for mask to increase OCR performance
- `constants.py`: Path and coordinates of the video
- `preprocess.py`: A module to preprocess OCR text results
- `video_download.py`: Pytube module to download youtube video using url
- `run.py`: A module to run the tracker
# Importing all necessary libraries
import cv2
import os
import pandas as pd

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image

# Read the video from specified path
VIDEO_PATH = "./data/video"
video_list = os.listdir(VIDEO_PATH)
API_KEY = 'AIzaSyBFc0XjsSHhnDpW-N0qtZ3uS11iLxxxx_g'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "op-gg-credential.json"


def pre_process(p_df):
    # 전처리 해주세요!!!


def detect_text(img, time):
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=img)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    temp_text = []
    vertex_0 = []
    vertex_1 = []
    vertex_2 = []
    vertex_3 = []

    for i in range(1, len(texts)):
        temp_text.append(texts[i].description)
        vertex_0.append((texts[i].bounding_poly.vertices[0].x,
                         texts[i].bounding_poly.vertices[0].y))
        vertex_1.append((texts[i].bounding_poly.vertices[1].x,
                         texts[i].bounding_poly.vertices[1].y))
        vertex_2.append((texts[i].bounding_poly.vertices[2].x,
                         texts[i].bounding_poly.vertices[2].y))
        vertex_3.append((texts[i].bounding_poly.vertices[3].x,
                         texts[i].bounding_poly.vertices[3].y))

    data = {'vertex_0': vertex_0, 'vertex_1': vertex_1,
            'vertex_2': vertex_2, 'vertex_3': vertex_3, 'text': temp_text}
    df = pd.DataFrame(data)
    m_df = pre_process(df)
    return m_df


# create image storage file if file doesn't exist
try:
    if not(os.path.isdir("./data/image)):
        os.makedirs(os.path.join("./data/image"))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

# frame
currentframe = 0
for video in video_list:
    cam = cv2.VideoCapture(VIDEO_PATH + "/" + video)
    while(True):
        # # reading from frame
        ret, frame = cam.read()
        if ret:
            success, encoded_image = cv2.imencode('.png', frame)
            content = encoded_image.tobytes()
            df = detect_text(content)
            currentframe += 1
            # DATA FRAME CONCAT 해야함!!!
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

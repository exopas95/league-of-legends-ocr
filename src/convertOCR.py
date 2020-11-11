# Importing all necessary libraries
import cv2
import os
import pandas as pd
import config

from bitwiseOperation import bit_operation
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image

# Read the video from specified path
VIDEO_PATH = "./data/video"
video_list = os.listdir(VIDEO_PATH)
API_KEY = 'AIzaSyBFc0XjsSHhnDpW-N0qtZ3uS11iLxxxx_g'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "op-gg-credential.json"


def inside_finder(coord, row, w, h):
    x1, x2, y1, y2 = coord[0]*w, coord[1]*w, coord[2]*h, coord[3]*h
    if (row.vertex_0[0] >= x1) & (row.vertex_0[1] >= y1) & (row.vertex_2[0] <= x2) & (row.vertex_0[1] <= y2):
        return True
    else:
        return False

def detect_text(content, w, h):
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=content)
    
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

    m_df = pd.DataFrame(data)
    
    d = {x:[] for x in list(config.coord_dict.keys())}
    df = pd.DataFrame(columns=list(config.coord_dict.keys())).T
    df['text_list'] = [[] for x in range(len(df))]
    
    for k, v in config.coord_dict.items() :
        for i, row in enumerate(m_df.itertuples()) :
            if inside_finder(v, row, w, h) :
                d[k].append(row.text)
        df.loc[k]['text_list'] = d[k]
    
    return df

# create image storage file if file doesn't exist
try:
    if not(os.path.isdir("./data/image")):
        os.makedirs(os.path.join("./data/image"))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

# frame
currentframe = 0
for video in video_list:
    cam = cv2.VideoCapture(VIDEO_PATH + "/" + video)
    df_result = pd.DataFrame(columns=config.cols).T
    while(True):
        ret, frame = cam.read()
        if ret:
            m_frame = bit_operation(frame)
            success, encoded_image = cv2.imencode('.png', m_frame)
            w, h = encoded_image.shape[1], encoded_image.shape[0]
            content = encoded_image.tobytes()
            df = detect_text(content, w, h)
            df_result['frame_'+str(currentframe)] = df.text_list
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()
    print(df_result)
    df.to_csv("opgg_data.csv", encoding="utf8")

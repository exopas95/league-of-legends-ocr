# Importing all necessary libraries
import cv2
import os
import pandas as pd
import src.config as config
# import config
# from bitwiseOperation import bit_operation
# video_list = os.listdir("C:\\Users\\Sewoong\\Desktop\\Develop\\opgg-ocr\\data\\video")

from src.bitwiseOperation import bit_operation
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from tqdm import tqdm

# Read the video from specified path
video_list = os.listdir(config.VIDEO_PATH)

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

    d = {x: [] for x in list(config.coord_dict.keys())}
    df = pd.DataFrame(columns=list(config.coord_dict.keys())).T
    df['text_list'] = [[] for x in range(len(df))]

    for k, v in config.coord_dict.items():
        for i, row in enumerate(m_df.itertuples()):
            if inside_finder(v, row, w, h):
                d[k].append(row.text)
        df.loc[k]['text_list'] = d[k]

    return df

def run():
    seconds = 30
    for video in video_list:
        cam = cv2.VideoCapture(config.VIDEO_PATH + "\\" + video)
        length = cam.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cam.get(cv2.CAP_PROP_FPS)
        multiplier = fps * seconds

        w, h = cam.get(3), cam.get(4)
        df_result = pd.DataFrame(columns=config.cols).T

        current_sec = 0
        p_frame = 0
        pbar = tqdm(total=int(length))
        while(True):
            ret, frame = cam.read()
            frameId = int(cam.get(1))

            if ret:
                if frameId % multiplier < 1:
                    m_frame = bit_operation(frame)
                    success, encoded_image = cv2.imencode('.png', m_frame)
                    content = encoded_image.tobytes()

                    df = detect_text(content, w, h)
                    df_result['frame_'+str(current_sec)] = df.text_list
                    current_sec += seconds

                    pbar.update(frameId - p_frame)
                    p_frame = frameId
            else:
                break

        pbar.close()
        cam.release()
        cv2.destroyAllWindows()
        df_result.to_csv(config.CSV_PATH + "\\" + video + ".csv", encoding="utf8")
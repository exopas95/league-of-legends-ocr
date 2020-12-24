# Importing all necessary libraries
import cv2
import os
import pandas as pd

import src.constants as constants
import src.preprocess as preprocess
import src.stats as stats
import src.db as db
from src.bitwise_operation import bit_operation

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from tqdm import tqdm

# Read the video from specified path
video_list = os.listdir(constants.VIDEO_PATH)

# Descriminate whether information we are looking for is inside the coordinates
def inside_finder(coord, row, w, h):
    x1, x2, y1, y2 = coord[0]*w, coord[1]*w, coord[2]*h, coord[3]*h
    if (row.vertex_0[0] >= x1) & (row.vertex_0[1] >= y1) & (row.vertex_2[0] <= x2) & (row.vertex_0[1] <= y2):
        return True
    else:
        return False

# Detect text from image using GCP Vision Intelligence
def detect_text(content, w, h, client):

    # GCP Vision Intelligence API
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # initialize lists
    temp_text = []
    vertex_0 = []
    vertex_1 = []
    vertex_2 = []
    vertex_3 = []

    # extract information for the reuslt
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

    # Create dataframe containing information from the results
    data = {'vertex_0': vertex_0, 'vertex_1': vertex_1, 'vertex_2': vertex_2, 'vertex_3': vertex_3, 'text': temp_text}
    data_df = pd.DataFrame(data)

    # Initialize dataframe and dictionary
    d = {x: [] for x in list(constants.coord_dict.keys())}
    df = pd.DataFrame(columns=list(constants.coord_dict.keys())).T
    df['text_list'] = [[] for x in range(len(df))]

    # Select necessary data from the result data frame
    for k, v in constants.coord_dict.items():
        for i, row in enumerate(data_df.itertuples()):
            if inside_finder(v, row, w, h):
                d[k].append(row.text)
        df.loc[k]['text_list'] = d[k]
    return df

# Main function
def run():
    # GCP Vision Intelligence API
    client = vision.ImageAnnotatorClient()

    seconds = 1                                                                         # Set frequency 
    for video in video_list:
        print(f"Start Processing: {video}")
        cam = cv2.VideoCapture(constants.VIDEO_PATH + "/" + video)                     # Video Capture start
        length = cam.get(cv2.CAP_PROP_FRAME_COUNT)                                      # Get the total number of the frames 
        fps = cam.get(cv2.CAP_PROP_FPS)                                                 # Get fps information of the video 
        multiplier = fps * seconds                                                      # Set multiplier

        w, h = cam.get(3), cam.get(4)                                                   # Get width and height information of the video
        df_result = pd.DataFrame(columns=constants.cols).T                              # Initialize data frame

        current_sec = 0                                                                 # Initialize time information   
        p_frame = 0                                                                     # Initialize previous frame id
        pbar = tqdm(total=int(length))                                                  # Set tqdm process bar
        
        # Process OCR on each frame
        while(cam.isOpened()):
            ret, frame = cam.read()                                                     # Get frame
            frameId = int(cam.get(1))                                                   # Get frame id of the current frame

            # If frame exists
            if ret:
                # Process image analysis according to the set frequency... ex) 10 sec
                if frameId % multiplier < 1:
                    video_timestamp = str(cam.get(cv2.CAP_PROP_POS_MSEC) / 1000)        # Count time
                    m_frame = bit_operation(frame)                                      # Mask current frame
                    success, encoded_image = cv2.imencode('.png', m_frame)              # Read image as png file
                    content = encoded_image.tobytes()                                   # Convert image from numpy to bytes

                    df = detect_text(content, w, h, client)                             # Process image OCR on the current frame
                    df_result['frame_'+str(current_sec)] = df.text_list                 # Update dataframe
                    df_result.loc["video_timestamp", 'frame_'+str(current_sec)] = video_timestamp
                    current_sec += seconds                                              # Update time information

                    pbar.update(frameId - p_frame)                                      # update tqdm process bar
                    p_frame = frameId                                                   # Save previous frame id
            
            # If frame does not exists
            else:
                break

        pbar.close()                                                                    # Close tqdm process bar
        cam.release()                                                                   # Close cv2 video catpure
        print(f"Video processed, Video Name: {video}")
#        cv2.destroyAllWindows()                                                         # Finish cv2
        df_result.T.to_csv(constants.CSV_PATH + "/raw_" + video + ".csv", encoding="utf8")                   

        processed_df = preprocess.result_process(df_result.T)     
        processed_df.to_csv(constants.CSV_PATH + "/" + video + ".csv", encoding="utf8")# Create csv file

        stats_df = stats.run(video)
        db.insert_row(stats_df)
        print(f"DataFrame created, Video Name: {video}")

    print("Completed")

import os

# directory path
CURRENT_PATH = os.getcwd()
VIDEO_PATH = CURRENT_PATH + "\\data\\video"
IMAGE_PATH = CURRENT_PATH + "\\data\\img"
CSV_PATH = CURRENT_PATH + "\\data\\csv"

# API KEY and credential for GCP
API_KEY = 'AIzaSyBFc0XjsSHhnDpW-N0qtZ3uS11iLxxxx_g'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CURRENT_PATH + \
    "\\op-gg-credential.json"

# Coordinates of the required information
coord_dict = {'blue_top_port': (0.0, 0.03646, 0.11111, 0.18519),
              'blue_jug_port': (0.0, 0.03646, 0.19444, 0.27778),
              'blue_mid_port': (0.0, 0.03646, 0.28704, 0.37963),
              'blue_bot_port': (0.0, 0.03646, 0.38889, 0.48148),
              'blue_sup_port': (0.0, 0.03646, 0.49074, 0.57407),
              'red_top_port': (0.96354, 1.0, 0.11111, 0.18519),
              'red_jug_port': (0.96354, 1.0, 0.19444, 0.27778),
              'red_mid_port': (0.96354, 1.0, 0.28704, 0.37963),
              'red_bot_port': (0.96354, 1.0, 0.38889, 0.48148),
              'red_sup_port': (0.96354, 1.0, 0.49074, 0.57407),
              'blue_teamgold': (0.33854, 0.42188, 0.0, 0.0463),
              'red_teamgold': (0.57292, 0.625, 0.0, 0.0463),
              'blue_killscore': (0.46875, 0.49479, 0.0, 0.0463),
              'red_killscore': (0.50521, 0.53125, 0.0, 0.0463),
              'timestamp': (0.48958, 0.51562, 0.05556, 0.09259),
              'notice': (0.26042, 0.72917, 0.18519, 0.25926),
              'blue_top_kda': (0.41667, 0.44792, 0.78704, 0.82407),
              'blue_jug_kda': (0.41667, 0.44792, 0.82407, 0.87037),
              'blue_mid_kda': (0.41667, 0.44792, 0.87037, 0.91667),
              'blue_bot_kda': (0.41667, 0.44792, 0.91667, 0.94444),
              'blue_sup_kda': (0.41667, 0.44792, 0.94444, 1.0),
              'blue_top_cs': (0.45312, 0.47917, 0.78704, 0.82407),
              'blue_jug_cs': (0.45312, 0.47917, 0.82407, 0.87037),
              'blue_mid_cs': (0.45312, 0.47917, 0.87037, 0.91667),
              'blue_bot_cs': (0.45312, 0.47917, 0.91667, 0.94444),
              'blue_sup_cs': (0.45312, 0.47917, 0.94444, 1.0),
              'red_top_kda': (0.55729, 0.58854, 0.78704, 0.82407),
              'red_jug_kda': (0.55729, 0.58854, 0.82407, 0.87037),
              'red_mid_kda': (0.55729, 0.58854, 0.87037, 0.91667),
              'red_bot_kda': (0.55729, 0.58854, 0.91667, 0.94444),
              'red_sup_kda': (0.55729, 0.58854, 0.94444, 1.0),
              'red_top_cs': (0.53125, 0.55208, 0.78704, 0.82407),
              'red_jug_cs': (0.53125, 0.55208, 0.82407, 0.87037),
              'red_mid_cs': (0.53125, 0.55208, 0.87037, 0.91667),
              'red_bot_cs': (0.53125, 0.55208, 0.91667, 0.94444),
              'red_sup_cs': (0.53125, 0.55208, 0.94444, 1.0),
              "blue_set_score":(0.189,0.229,0.006,0.03), 
              "red_set_score":(0.776,0.818,0.006,0.03),
              "blue_top_vision_score":(0.305,0.33,0.813,0.828),
              "blue_jug_vision_score":(0.305,0.33,0.853,0.868),
              "blue_mid_vision_score":(0.305,0.33,0.893,0.908),
              "blue_bot_vision_score":(0.305,0.33,0.933,0.948),
              "blue_sup_vision_score":(0.305,0.33,0.973,0.988),
              "red_top_vision_score":(0.673,0.702,0.813,0.828),
              "red_jug_vision_score":(0.673,0.702,0.853,0.868),
              "red_mid_vision_score":(0.673,0.702,0.893,0.908),
              "red_bot_vision_score":(0.673,0.702,0.933,0.948),
              "red_sup_vision_score":(0.673,0.702,0.973,0.988),
              "blue_tower_score":(0.332,0.361,0.015,0.03),
              "red_tower_score":(0.656,0.685,0.015,0.03)
              }

# Column information of the dataframe
cols = ['blue_top_port', 'blue_jug_port', 'blue_mid_port', 'blue_bot_port',
        'blue_sup_port', 'red_top_port', 'red_jug_port', 'red_mid_port',
        'red_bot_port', 'red_sup_port', 'blue_teamgold', 'red_teamgold',
        'blue_killscore', 'red_killscore', 'timestamp', 'notice',
        'blue_top_kda', 'blue_jug_kda', 'blue_mid_kda', 'blue_bot_kda',
        'blue_sup_kda', 'blue_top_cs', 'blue_jug_cs', 'blue_mid_cs',
        'blue_bot_cs', 'blue_sup_cs', 'red_top_kda', 'red_jug_kda',
        'red_mid_kda', 'red_bot_kda', 'red_sup_kda', 'red_top_cs',
        'red_jug_cs', 'red_mid_cs', 'red_bot_cs', 'red_sup_cs']

# Vectors of level, tower, socre_board location
vec = {
        "level":[(0.003, 0.171),(0.003, 0.266),(0.003, 0.362),
                    (0.003, 0.456),(0.003, 0.552),(0.984, 0.171),
                (0.984, 0.266),(0.984, 0.362),(0.984, 0.456),(0.984, 0.552)],\
        "tower_score":[(0.333, 0.016),(0.667, 0.016)],\
        "set_score":[(0.189, 0.007),(0.786, 0.007)],\
        "vision_score":[(0.306, 0.815),(0.306, 0.856),(0.306, 0.896),
                      (0.306, 0.936),(0.306, 0.977),(0.686, 0.815),
                      (0.686, 0.856),(0.686, 0.896),(0.686, 0.936),(0.686, 0.977)]}


import os

# directory path
CURRENT_PATH = os.getcwd()
VIDEO_PATH = CURRENT_PATH + "\\data\\video"
IMAGE_PATH = CURRENT_PATH + "\\data\\img"
CSV_PATH = CURRENT_PATH + "\\data\\csv"
SECONDS = 1

# API KEY and credential for GCP
API_KEY = 'AIzaSyBFc0XjsSHhnDpW-N0qtZ3uS11iLxxxx_g'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CURRENT_PATH + \
    "\\op-gg-credential.json"

# Coordinates of the required information
coord_dict = {
              # Top - Menu bar & Notice
              "blue_set_score" :(0.189,0.229,0.006,0.035), 
              "red_set_score" :(0.776,0.818,0.006,0.035),
              'blue_teamgold': (0.37854, 0.42188, 0.0, 0.0463),
              'red_teamgold': (0.57292, 0.625, 0.0, 0.0463),
              'blue_killscore': (0.46875, 0.49479, 0.0, 0.0463),
              'red_killscore': (0.50521, 0.53125, 0.0, 0.0463),
              'timestamp': (0.48958, 0.51562, 0.05556, 0.09259),
              "blue_tower_score": (0.332,0.361,0.015,0.035),
              "red_tower_score": (0.656,0.685,0.015,0.035),
              "left_top_dragon_info": (0.01,0.131,0.015,0.101),
              'notice': (0.26042, 0.72917, 0.18519, 0.25926),

              # Left, Right - Player name & Lvl
              'blue_top_port': (0.0, 0.05546, 0.11111, 0.18519),
              'blue_jug_port': (0.0, 0.05546, 0.19444, 0.28078),
              'blue_mid_port': (0.0, 0.05546, 0.28704, 0.37963),
              'blue_bot_port': (0.0, 0.05546, 0.38889, 0.48148),
              'blue_sup_port': (0.0, 0.05546, 0.49074, 0.57407),
              'red_top_port': (0.94054, 1.0, 0.11111, 0.18519),
              'red_jug_port': (0.94054, 1.0, 0.19444, 0.28078),
              'red_mid_port': (0.94054, 1.0, 0.28704, 0.37963),
              'red_bot_port': (0.94054, 1.0, 0.38889, 0.48148),
              'red_sup_port': (0.94054, 1.0, 0.49074, 0.57407),

              # Bottom - KDA
              'blue_top_kda': (0.41667, 0.44792, 0.8035, 0.8244),
              'blue_jug_kda': (0.41667, 0.44792, 0.8444, 0.8645),
              'blue_mid_kda': (0.41667, 0.44792, 0.8845, 0.9045),
              'blue_bot_kda': (0.41667, 0.44792, 0.9245, 0.9445),
              'blue_sup_kda': (0.41667, 0.44792, 0.9645, 1.0),
              'red_top_kda': (0.55729, 0.586, 0.8035, 0.8244),
              'red_jug_kda': (0.55729, 0.586, 0.8444, 0.8645),
              'red_mid_kda': (0.55729, 0.586, 0.8845, 0.9045),
              'red_bot_kda': (0.55729, 0.586, 0.9245, 0.9445),
              'red_sup_kda': (0.55729, 0.586, 0.9645, 1.0),

              # Bottom - CS
              'blue_top_cs': (0.45312, 0.48017, 0.78704, 0.82407),
              'blue_jug_cs': (0.45312, 0.48017, 0.82407, 0.87037),
              'blue_mid_cs': (0.45312, 0.48017, 0.87037, 0.91667),
              'blue_bot_cs': (0.45312, 0.48017, 0.91667, 0.94444),
              'blue_sup_cs': (0.45312, 0.48017, 0.94444, 1.0),
              'red_top_cs': (0.53125, 0.55208, 0.78704, 0.82407),
              'red_jug_cs': (0.53125, 0.55208, 0.82407, 0.87037),
              'red_mid_cs': (0.53125, 0.55208, 0.87037, 0.91667),
              'red_bot_cs': (0.53125, 0.55208, 0.91667, 0.94444),
              'red_sup_cs': (0.53125, 0.55208, 0.94444, 1.0),

              # Bottom - Vision score
              "blue_top_vision_score": (0.305,0.333,0.813,0.828),
              "blue_jug_vision_score": (0.305,0.333,0.853,0.868),
              "blue_mid_vision_score": (0.305,0.333,0.893,0.908),
              "blue_bot_vision_score": (0.305,0.333,0.933,0.948),
              "blue_sup_vision_score": (0.305,0.333,0.973,0.988),
              "red_top_vision_score": (0.673,0.702,0.813,0.828),
              "red_jug_vision_score": (0.673,0.702,0.853,0.868),
              "red_mid_vision_score": (0.673,0.702,0.893,0.908),
              "red_bot_vision_score": (0.673,0.702,0.933,0.948),
              "red_sup_vision_score": (0.673,0.702,0.973,0.988),

              # Bottom - Shutdown gold
              "blue_top_shutdown" : (0.41667,0.44802,0.7835,0.8035),
              "blue_jug_shutdown" : (0.41667,0.44802,0.8244,0.8444),
              "blue_mid_shutdown" : (0.41667,0.44802,0.8645,0.8845),
              "blue_bot_shutdown" : (0.41667,0.44802,0.9045,0.9245),
              "blue_sup_shutdown" : (0.41667,0.44802,0.9445,0.9645),
              "red_top_shutdown" : (0.55729,0.586,0.7835,0.8035),
              "red_jug_shutdown" : (0.55729,0.586,0.8244,0.8444),
              "red_mid_shutdown" : (0.55729,0.586,0.8645,0.8845),
              "red_bot_shutdown" : (0.55729,0.586,0.9045,0.9245),
              "red_sup_shutdown" : (0.55729,0.586,0.9445,0.9645),
              }

coord_dict_LCS = {
                    # Top - Menu bar & Notice
                    "blue_set_score" :(0.26,0.30,0.035,0.06), 
                    "red_set_score" :(0.7,0.745,0.035,0.06),
                    'blue_teamgold': (0.42, 0.47, 0.0, 0.0463),
                    'red_teamgold': (0.53, 0.58, 0.0, 0.0463),
                    'blue_killscore': (0.385, 0.41, 0.015, 0.042),
                    'red_killscore': (0.60, 0.625, 0.015, 0.042),
                    'timestamp': (0.48958, 0.51562, 0.05556, 0.09259),
                    "blue_tower_score": (0.33,0.365,0.015,0.042),
                    "red_tower_score": (0.65,0.685,0.015,0.042),
                    "left_top_dragon_info": (0.01,0.131,0.015,0.101),
                    'notice': (0.26042, 0.72917, 0.18519, 0.25926),

                    # Left, Right - Player name & Lvl
                    'blue_top_port': (0.0, 0.05546, 0.11111, 0.18519),
                    'blue_jug_port': (0.0, 0.05546, 0.19444, 0.28078),
                    'blue_mid_port': (0.0, 0.05546, 0.28704, 0.37963),
                    'blue_bot_port': (0.0, 0.05546, 0.38889, 0.48148),
                    'blue_sup_port': (0.0, 0.05546, 0.49074, 0.57407),
                    'red_top_port': (0.94054, 1.0, 0.11111, 0.18519),
                    'red_jug_port': (0.94054, 1.0, 0.19444, 0.28078),
                    'red_mid_port': (0.94054, 1.0, 0.28704, 0.37963),
                    'red_bot_port': (0.94054, 1.0, 0.38889, 0.48148),
                    'red_sup_port': (0.94054, 1.0, 0.49074, 0.57407),

                    # Bottom - KDA
                    'blue_top_kda': (0.41667, 0.44792, 0.8035, 0.8244),
                    'blue_jug_kda': (0.41667, 0.44792, 0.8444, 0.8645),
                    'blue_mid_kda': (0.41667, 0.44792, 0.8845, 0.9045),
                    'blue_bot_kda': (0.41667, 0.44792, 0.9245, 0.9445),
                    'blue_sup_kda': (0.41667, 0.44792, 0.9645, 1.0),
                    'red_top_kda': (0.55729, 0.586, 0.8035, 0.8244),
                    'red_jug_kda': (0.55729, 0.586, 0.8444, 0.8645),
                    'red_mid_kda': (0.55729, 0.586, 0.8845, 0.9045),
                    'red_bot_kda': (0.55729, 0.586, 0.9245, 0.9445),
                    'red_sup_kda': (0.55729, 0.586, 0.9645, 1.0),

                    # Bottom - CS
                    'blue_top_cs': (0.45312, 0.48017, 0.78704, 0.82407),
                    'blue_jug_cs': (0.45312, 0.48017, 0.82407, 0.87037),
                    'blue_mid_cs': (0.45312, 0.48017, 0.87037, 0.91667),
                    'blue_bot_cs': (0.45312, 0.48017, 0.91667, 0.94444),
                    'blue_sup_cs': (0.45312, 0.48017, 0.94444, 1.0),
                    'red_top_cs': (0.53125, 0.55208, 0.78704, 0.82407),
                    'red_jug_cs': (0.53125, 0.55208, 0.82407, 0.87037),
                    'red_mid_cs': (0.53125, 0.55208, 0.87037, 0.91667),
                    'red_bot_cs': (0.53125, 0.55208, 0.91667, 0.94444),
                    'red_sup_cs': (0.53125, 0.55208, 0.94444, 1.0),

                    # Bottom - Vision score
                    "blue_top_vision_score": (0.305,0.335,0.813,0.828),
                    "blue_jug_vision_score": (0.305,0.335,0.853,0.868),
                    "blue_mid_vision_score": (0.305,0.335,0.893,0.908),
                    "blue_bot_vision_score": (0.305,0.335,0.933,0.948),
                    "blue_sup_vision_score": (0.305,0.335,0.973,0.988),
                    "red_top_vision_score": (0.67,0.702,0.813,0.828),
                    "red_jug_vision_score": (0.67,0.702,0.853,0.868),
                    "red_mid_vision_score": (0.67,0.702,0.893,0.908),
                    "red_bot_vision_score": (0.67,0.702,0.933,0.948),
                    "red_sup_vision_score": (0.67,0.702,0.973,0.988),

                    # Bottom - Shutdown gold
                    "blue_top_shutdown" : (0.41667,0.44802,0.7835,0.8035),
                    "blue_jug_shutdown" : (0.41667,0.44802,0.8244,0.8444),
                    "blue_mid_shutdown" : (0.41667,0.44802,0.8645,0.8845),
                    "blue_bot_shutdown" : (0.41667,0.44802,0.9045,0.9245),
                    "blue_sup_shutdown" : (0.41667,0.44802,0.9445,0.9645),
                    "red_top_shutdown" : (0.55729,0.586,0.7835,0.8035),
                    "red_jug_shutdown" : (0.55729,0.586,0.8244,0.8444),
                    "red_mid_shutdown" : (0.55729,0.586,0.8645,0.8845),
                    "red_bot_shutdown" : (0.55729,0.586,0.9045,0.9245),
                    "red_sup_shutdown" : (0.55729,0.586,0.9445,0.9645),
                }

coord_dict_LEC = {
                # Top - Menu bar & Notice
                "blue_set_score" :(0.189,0.229,0.006,0.03), 
                "red_set_score" :(0.776,0.818,0.006,0.03),
                'blue_teamgold': (0.38354, 0.42188, 0.0, 0.0463), 
                'red_teamgold': (0.59292, 0.635, 0.0, 0.0463), 
                'blue_killscore': (0.46875, 0.49479, 0.0, 0.0463),
                'red_killscore': (0.50521, 0.53125, 0.0, 0.0463),
                'timestamp': (0.48958, 0.51562, 0.05556, 0.09259),
                "blue_tower_score": (0.332,0.361,0.015,0.04),
                "red_tower_score": (0.656,0.685,0.015,0.04),
                "left_top_dragon_info": (0.01,0.131,0.015,0.101),
                'notice': (0.26042, 0.72917, 0.18519, 0.25926),

                # Left, Right - Player name & Lvl
                'blue_top_port': (0.0, 0.05546, 0.11111, 0.18519),
                'blue_jug_port': (0.0, 0.05546, 0.19444, 0.27778),
                'blue_mid_port': (0.0, 0.05546, 0.28704, 0.37963),
                'blue_bot_port': (0.0, 0.05546, 0.38889, 0.48148),
                'blue_sup_port': (0.0, 0.05546, 0.49074, 0.57407),
                'red_top_port': (0.94054, 1.0, 0.11111, 0.18519),
                'red_jug_port': (0.94054, 1.0, 0.19444, 0.27778),
                'red_mid_port': (0.94054, 1.0, 0.28704, 0.37963),
                'red_bot_port': (0.94054, 1.0, 0.38889, 0.48148),
                'red_sup_port': (0.94054, 1.0, 0.49074, 0.57407),

                # Bottom - KDA
                'blue_top_kda': (0.41667, 0.44792, 0.790, 0.815),
                'blue_jug_kda': (0.41667, 0.44792, 0.832, 0.857),
                'blue_mid_kda': (0.41667, 0.44792, 0.874, 0.900),
                'blue_bot_kda': (0.41667, 0.44792, 0.917, 0.947),
                'blue_sup_kda': (0.41667, 0.44792, 0.964, 1.0),
                'red_top_kda': (0.55729, 0.58854, 0.790, 0.815),
                'red_jug_kda': (0.55729, 0.58854, 0.832, 0.857),
                'red_mid_kda': (0.55729, 0.58854, 0.874, 0.900),
                'red_bot_kda': (0.55729, 0.58854, 0.917, 0.947),
                'red_sup_kda': (0.55729, 0.58854, 0.964, 1.0),

                # Bottom - CS
                'blue_top_cs': (0.45312, 0.47917, 0.78704, 0.82407),
                'blue_jug_cs': (0.45312, 0.47917, 0.82407, 0.87037),
                'blue_mid_cs': (0.45312, 0.47917, 0.87037, 0.91667),
                'blue_bot_cs': (0.45312, 0.47917, 0.91667, 0.94444),
                'blue_sup_cs': (0.45312, 0.47917, 0.94444, 1.0),
                'red_top_cs': (0.53125, 0.55208, 0.78704, 0.82407),
                'red_jug_cs': (0.53125, 0.55208, 0.82407, 0.87037),
                'red_mid_cs': (0.53125, 0.55208, 0.87037, 0.91667),
                'red_bot_cs': (0.53125, 0.55208, 0.91667, 0.94444),
                'red_sup_cs': (0.53125, 0.55208, 0.94444, 1.0),

                # Bottom - Vision score
                "blue_top_vision_score": (0.295,0.323,0.801,0.816),
                "blue_jug_vision_score": (0.295,0.323,0.843,0.858),
                "blue_mid_vision_score": (0.295,0.323,0.885,0.900),
                "blue_bot_vision_score": (0.295,0.323,0.933,0.948),
                "blue_sup_vision_score": (0.295,0.323,0.973,0.988),
                "red_top_vision_score": (0.682,0.715,0.801,0.816),
                "red_jug_vision_score": (0.682,0.715,0.843,0.858),
                "red_mid_vision_score": (0.682,0.715,0.885,0.900),
                "red_bot_vision_score": (0.682,0.715,0.933,0.948),
                "red_sup_vision_score": (0.682,0.715,0.973,0.988),

                # Bottom - Shutdown gold
                "blue_top_shutdown" : (0.41667,0.44792,0.773,0.790),
                "blue_jug_shutdown" : (0.41667,0.44792,0.815,0.832),
                "blue_mid_shutdown" : (0.41667,0.44792,0.857,0.874),
                "blue_bot_shutdown" : (0.41667,0.44792,0.900,0.917),
                "blue_sup_shutdown" : (0.41667,0.44792,0.947,0.964),
                "red_top_shutdown" : (0.55729,0.58854,0.773,0.790),
                "red_jug_shutdown" : (0.55729,0.58854,0.815,0.832),
                "red_mid_shutdown" : (0.55729,0.58854,0.857,0.874),
                "red_bot_shutdown" : (0.55729,0.58854,0.900,0.917),
                "red_sup_shutdown" : (0.55729,0.58854,0.947,0.964),
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
        'red_jug_cs', 'red_mid_cs', 'red_bot_cs', 'red_sup_cs',
        'blue_set_score', 'red_set_score','blue_top_vision_score','blue_jug_vision_score',
        'blue_mid_vision_score','blue_bot_vision_score','blue_sup_vision_score',
        'red_top_vision_score','red_jug_vision_score','red_mid_vision_score',
        'red_bot_vision_score','red_sup_vision_score','blue_top_shutdown', 'blue_jug_shutdown',
        'blue_mid_shutdown', 'blue_bot_shutdown', 'blue_sup_shutdown', 'red_top_shutdown',
        'red_jug_shutdown', 'red_mid_shutdown', 'red_bot_shutdown', 'red_sup_shutdown',
        'blue_tower_score','red_tower_score',
        "left_top_dragon_info"]

# Vectors of level, tower, socre_board location
vec = {
        "level":[(0.003, 0.171),(0.003, 0.266),(0.003, 0.362),(0.003, 0.456),(0.003, 0.552),
                 (0.984, 0.171),(0.984, 0.266),(0.984, 0.362),(0.984, 0.456),(0.984, 0.552)],\
        "tower_score":[(0.333, 0.016),(0.667, 0.016)],\
        "set_score":[(0.189, 0.007),(0.786, 0.007)],\
        "vision_score":[(0.305, 0.815),(0.305, 0.856),(0.305, 0.896),(0.305, 0.936),(0.305, 0.977),
                        (0.687, 0.815),(0.687, 0.856),(0.687, 0.896),(0.687, 0.936),(0.687, 0.977)]}

vec_LCS = {
        "level":[(0.003, 0.171),(0.003, 0.266),(0.003, 0.362),(0.003, 0.456),(0.003, 0.552),
                 (0.984, 0.171),(0.984, 0.266),(0.984, 0.362),(0.984, 0.456),(0.984, 0.552)],\
        "tower_score":[(0.33, 0.024),(0.667, 0.024)],\
        "set_score":[(0.26, 0.035),(0.712, 0.035)],\
        "vision_score":[(0.305, 0.815),(0.305, 0.856),(0.305, 0.896),(0.305, 0.936),(0.305, 0.977),
                      (0.687, 0.815),(0.687, 0.856),(0.687, 0.896),(0.687, 0.936),(0.687, 0.977)]}

vec_LEC = {
        "level":[(0.003, 0.171),(0.003, 0.266),(0.003, 0.362),(0.003, 0.456),(0.003, 0.552),
                 (0.984, 0.171),(0.984, 0.266),(0.984, 0.362),(0.984, 0.456),(0.984, 0.552)],\
        "tower_score":[(0.333, 0.018),(0.667, 0.018)],\
        "set_score":[(0.189, 0.007),(0.786, 0.007)],\
        "vision_score":[(0.295, 0.803),(0.295, 0.846),(0.295, 0.888),(0.295, 0.933),(0.295, 0.976),
                        (0.698, 0.803),(0.698, 0.846),(0.698, 0.888),(0.698, 0.933),(0.698, 0.976)]}
    
# main text
total_sentence = {
    'start_sentence' : '소환사의협곡에오신것을환영합니다',
    'minion_30_sentence' : '미니언생성까지초남았습니다',
    'minion_sentence' : '미니언이생성 되었습니다',
    'first_blood_sentence' : '선취점',
    'kill_sentence_kv_0' : '님이님을처치했습니다',
    'kill_sentence_k_0' : '님이학살중입니다',
    'kill_sentence_k_1' : '님을도저히막을수없습니다',
    'kill_sentence_n_0' : '연속킬차단',
    'kill_sentence_k_2' : '님이미쳐날뛰고있습니다',
    'kill_sentence_n_1' :  '마지막적처치',
    'kill_sentence_n_2' : '더블킬',
    'kill_sentence_n_3' : '트리플킬',
    'kill_sentence_n_4' : '쿼드라킬',
    'kill_sentence_n_5' : '펜타킬',
    'red_dragon_sentence' : '빨강팀이드래곤을처치했습니다',
    'blue_dragon_sentence' : '파랑팀이드래곤을처치했습니다',
    'blue_tower_sentence' : '빨강팀의포탑이파괴되었습니다',
    'red_tower_sentence' : '파랑팀포탑이파괴되었습니다',
    'blue_first_tower_sentence' : '파랑팀이첫번째포탑을파괴했습니다',
    'red_first_tower_sentence' : '빨강팀이첫번째포탑을파괴했습니다',
    #herald_sentence = ??
    'herald_summon_sentence' : '팀이협곡의전령을소환했습니다',
    'nashor_sentence' : '팀이내셔남작을처치했습니다',
    #억제기
    'inhibitor_sentence' : '님이팀억제기를파괴했습니다'
    }

text_str = ['start_sentence', 'minion_30_sentence', 'minion_sentence', 'first_blood_sentence',
            'kill_sentence_kv_0', 'kill_sentence_k_0', 'kill_sentence_k_1', 'kill_sentence_n_0', 'kill_sentence_k_2',
            'kill_sentence_n_1', 'kill_sentence_n_2', 'kill_sentence_n_3', 'kill_sentence_n_4', 'kill_sentence_n_5',
            'red_dragon_sentence', 'blue_dragon_sentence', 'blue_tower_sentence',
            'red_tower_sentence', 'blue_first_tower_sentence', 'red_first_tower_sentence',
            'herald_summon_sentence', 'nashor_sentence', 'inhibitor_sentence']    
    
# english main text
eng_total_sentence = {
    'start_sentence' : 'welcome to summoner\'s rift',
    'minion_30_sentence' : 'thirty seconds until minions spawn',
    'minion_sentence' : 'minions have spawned',
    'kill_sentence' : 'has slain',
    'blue_tower_sentence' : 'red turret destroyed',
    'red_tower_sentence' : 'blue turret destroyed',
    'blue_first_tower_sentence' : 'blue team destroyed the first turret',
    'red_first_tower_sentence' : 'red team destroyed the first turret'
    }

eng_text_str = ['start_sentence', 'minion_30_sentence', 'minion_sentence', 
            'kill_sentence', 'blue_tower_sentence', 'red_tower_sentence', 
            'blue_first_tower_sentence', 'red_first_tower_sentence',
           ]

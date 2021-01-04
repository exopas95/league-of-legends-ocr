import pandas as pd
import numpy as np
import json
import re
import src.preprocess as preprocess



def static_info_json(raw_df,df):
    raw = preprocess.get_game_df(raw_df)
    df = df.copy()
    cols = {
        'preprocess_cols' : [            
            'blue_team',
            'blue_top_player',
            'blue_jug_player',
            'blue_mid_player',
            'blue_bot_player',        
            'blue_sup_player',               
            'blue_drake',
            'blue_nashor',
            'blue_summon_herald',
            'blue_set_score',
            'red_team',
            'red_top_player',
            'red_jug_player',
            'red_mid_player',
            'red_bot_player',        
            'red_sup_player',               
            'red_drake',
            'red_nashor',
            'red_summon_herald',
            'red_set_score'
        ]
    } 

    df_dict={}
    
    def judge_name(x, side):  
        try:
            if np.isnan(x):
                return ' '.join(x)
        except:
            words = ' '.join(x)
            word = re.sub('[^a-zA-Z가-힣0-9- ]+', '', words)
            word = word.split(' ')
            if side == 'blue':
                ptp_name = word[:2]
            elif side == 'red':
                ptp_name = word[:2]
            return ' '.join(ptp_name)


    def get_name(df, side, pos):
        l=[]
        for i in cols['preprocess_cols']:
            if 'player' in i:
                for x in df[side+'_'+pos+'_port'].values :
                    if len(x)>=3:
                        l.append(judge_name(x, side))
                    else:
                        l.append('')
        return max(set(l), key = l.count).rstrip().lstrip()

    for i in cols['preprocess_cols']:
        if 'team' in i:
            df_dict[i] = get_name(raw, i[:i.find('_')], 'top').split(' ')[0]
        elif 'player' in i:
            try:
                df_dict[i] = ' '.join(get_name(raw, i[:i.find('_')], i[i.find('_')+1:i.rfind('_')]).split(' ')[1:])
            except:
                df_dict[i] = ' '.join(get_name(raw, i[:i.find('_')], i[i.find('_')+1:i.rfind('_')]))    

    static_dict = dict.fromkeys(cols['preprocess_cols'],None)
    
    for i in cols['preprocess_cols']:
        if 'blue' in i:
            if 'set_score' in i:
                try:
                    static_dict[i] = int(raw_df[raw_df.blue_set_score.str.len()==8]['blue_set_score'].mode().iloc[0][5:6])
                except:
                    static_dict[i] = np.nan
            elif 'drake' in i:
                static_dict[i] = df['100_drake'].dropna().tolist()
            elif 'nashor' in i:
                static_dict[i] = df['100_nashor_herald'].dropna().tolist().count('nashor')
            elif 'summon' in i:
                static_dict[i] = df['100_nashor_herald'].dropna().tolist().count('summon_herald')
            else:
                static_dict[i] = df_dict[i]
        if 'red' in i:
            if 'set_score' in i:
                try:
                    static_dict[i] = int(raw_df[raw_df.red_set_score.str.len()==8]['red_set_score'].mode().iloc[0][2:3])
                except:
                    static_dict[i] = np.nan
            elif 'drake' in i:
                static_dict[i] = df['200_drake'].dropna().tolist()
            elif 'nashor' in i:
                static_dict[i] = df['200_nashor_herald'].dropna().tolist().count('nashor')
            elif 'summon' in i:
                static_dict[i] = df['200_nashor_herald'].dropna().tolist().count('summon_herald')
            else:
                static_dict[i] = df_dict[i]
                
    
    static_info = {
        "teams": [
            {
                "team_id": 100,
                "team_name": static_dict['blue_team'],
                "object_info": {
                    'drake':static_dict['blue_drake'],
                    'nashor':static_dict['blue_nashor'],
                    'summon_herald':static_dict['blue_summon_herald']
                    },
                "set_score": static_dict['blue_set_score']
            },
            {
                "team_id": 200,
                "team_name": static_dict['red_team'],
                "object_info": {
                    'drake':static_dict['red_drake'],
                    'nashor':static_dict['red_nashor'],
                    'summon_herald':static_dict['red_summon_herald']
                    },
                "set_score": static_dict['red_set_score']
            }
        ],
        "participants": [
            {
                "participant_id": 1,
                "team_id": 100,
                "position": "TOP",
                "summoner_name": static_dict['blue_top_player']
            },
            {
                "participant_id": 2,
                "team_id": 100,
                "position": "JUG",
                "summoner_name": static_dict['blue_jug_player']
            },
            {
                "participant_id": 3,
                "team_id": 100,
                "position": "MID",
                "summoner_name": static_dict['blue_mid_player']
            },
            {
                "participant_id": 4,
                "team_id": 100,
                "position": "BOT",
                "summoner_name": static_dict['blue_bot_player']
            },
            {
                "participant_id": 5,
                "team_id": 100,
                "position": "SUP",
                "summoner_name": static_dict['blue_sup_player']
            },
            {
                "participant_id": 6,
                "team_id": 200,
                "position": "TOP",
                "summoner_name": static_dict['red_top_player']
            },
            {
                "participant_id": 7,
                "team_id": 200,
                "position": "JUG",
                "summoner_name": static_dict['red_jug_player']
            },
            {
                "participant_id": 8,
                "team_id": 200,
                "position": "MID",
                "summoner_name": static_dict['red_mid_player']
            },
            {
                "participant_id": 9,
                "team_id": 200,
                "position": "BOT",
                "summoner_name": static_dict['red_bot_player']
            },
            {
                "participant_id": 10,
                "team_id": 200,
                "position": "SUP",
                "summoner_name": static_dict['red_sup_player']
            },
        ]           
 
    }
    return static_info




def make_json_df(df):
    final= df
    final = final.set_index('video_timestamp', drop=True)
    return final


def make_json_file(raw_df, df):
    
    static_info = static_info_json(raw_df, df)
    
    final = make_json_df(df)
    df_dict= final.T.to_dict()
    
    
    #make each participant info from dataframe
    
    red_top_level = final['206_level'].tolist()
    blue_top_level = final['101_level'].tolist()
    red_jug_level = final['207_level'].tolist()
    blue_jug_level = final['102_level'].tolist()
    red_mid_level = final['208_level'].tolist()
    blue_mid_level = final['103_level'].tolist()
    red_bot_level = final['209_level'].tolist()
    blue_bot_level = final['104_level'].tolist()
    red_sup_level = final['210_level'].tolist()
    blue_sup_level = final['105_level'].tolist()


    blue_top_cs = final['101_cs'].tolist()
    blue_jug_cs = final['102_cs'].tolist()
    blue_mid_cs = final['103_cs'].tolist()
    blue_bot_cs = final['104_cs'].tolist()
    blue_sup_cs = final['105_cs'].tolist()


    red_top_cs = final['206_cs'].tolist()
    red_jug_cs = final['207_cs'].tolist()
    red_mid_cs = final['208_cs'].tolist()
    red_bot_cs = final['209_cs'].tolist()
    red_sup_cs = final['210_cs'].tolist()


    blue_top_k = final['101_k'].tolist()
    blue_top_d = final['101_d'].tolist()
    blue_top_a = final['101_a'].tolist()
    blue_jug_k = final['102_k'].tolist()
    blue_jug_d = final['102_d'].tolist()
    blue_jug_a = final['102_a'].tolist()
    blue_mid_k = final['103_k'].tolist()
    blue_mid_d = final['103_d'].tolist()
    blue_mid_a = final['103_a'].tolist()
    blue_bot_k = final['104_k'].tolist()
    blue_bot_d = final['104_d'].tolist()
    blue_bot_a = final['104_a'].tolist()
    blue_sup_k = final['105_k'].tolist()
    blue_sup_d = final['105_d'].tolist()
    blue_sup_a = final['105_a'].tolist()



    red_top_k = final['206_k'].tolist()
    red_top_d = final['206_d'].tolist()
    red_top_a = final['206_a'].tolist()
    red_jug_k = final['207_k'].tolist()
    red_jug_d = final['207_d'].tolist()
    red_jug_a = final['207_a'].tolist()
    red_mid_k = final['208_k'].tolist()
    red_mid_d = final['208_d'].tolist()
    red_mid_a = final['208_a'].tolist()
    red_bot_k = final['209_k'].tolist()
    red_bot_d = final['209_d'].tolist()
    red_bot_a = final['209_a'].tolist()
    red_sup_k = final['210_k'].tolist()
    red_sup_d = final['210_d'].tolist()
    red_sup_a = final['210_a'].tolist()




    blue_top_vision_score = final['101_vision_score'].tolist()
    blue_jug_vision_score = final['102_vision_score'].tolist()
    blue_mid_vision_score = final['103_vision_score'].tolist()
    blue_bot_vision_score = final['104_vision_score'].tolist()
    blue_sup_vision_score = final['105_vision_score'].tolist()

    red_top_vision_score = final['206_vision_score'].tolist()
    red_jug_vision_score = final['207_vision_score'].tolist()
    red_mid_vision_score = final['208_vision_score'].tolist()
    red_bot_vision_score = final['209_vision_score'].tolist()
    red_sup_vision_score = final['210_vision_score'].tolist()



    red_teamgold= final['200_teamgold'].tolist()
    blue_teamgold= final['100_teamgold'].tolist()


    red_drake= final['200_drake'].fillna(0).tolist()
    blue_drake= final['100_drake'].fillna(0).tolist()

    red_nashor_herald = final['200_nashor_herald'].fillna(0).tolist()
    blue_nashor_herald = final['100_nashor_herald'].fillna(0).tolist()

    blue_tower_score = final['100_tower_score'].tolist()
    red_tower_score = final['200_tower_score'].tolist()


    killer = final['killer'].tolist()
    victim = final['victim'].tolist()

    
    
    
    
    video_dict = dict()  
    video_dict['frames'] = list()
    for key in df_dict:
        video_dict['frames'].append(dict())   # make overall frame of dictionary
        
    video_timestamp = [v for i,v in enumerate(df_dict)]
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['video_timestamp'] = video_timestamp[index] #insert video_timestamp data
        
    timestamp = final.index.tolist()
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['ingame_timestamp'] = timestamp[index] #insert ingame_timestamp data
    
    for frame in video_dict['frames']:
        frame['data']= dict()
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['team_info'] = list()
        video_dict['frames'][index]['data']['participant_info'] = list()
        video_dict['frames'][index]['data']['fight'] = dict()  #make frames for 'data'
        
    
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['team_info'].append(dict())
        video_dict['frames'][index]['data']['team_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
        video_dict['frames'][index]['data']['participant_info'].append(dict())
    
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['team_info'][0]['team_id'] = 100
        video_dict['frames'][index]['data']['team_info'][1]['team_id'] = 200
        video_dict['frames'][index]['data']['participant_info'][0]["participant_id"]= 1
        video_dict['frames'][index]['data']['participant_info'][1]["participant_id"]= 2
        video_dict['frames'][index]['data']['participant_info'][2]["participant_id"]= 3
        video_dict['frames'][index]['data']['participant_info'][3]["participant_id"]= 4
        video_dict['frames'][index]['data']['participant_info'][4]["participant_id"]= 5
        video_dict['frames'][index]['data']['participant_info'][5]["participant_id"]= 6
        video_dict['frames'][index]['data']['participant_info'][6]["participant_id"]= 7
        video_dict['frames'][index]['data']['participant_info'][7]["participant_id"]= 8
        video_dict['frames'][index]['data']['participant_info'][8]["participant_id"]= 9
        video_dict['frames'][index]['data']['participant_info'][9]["participant_id"]= 10
    
    
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['team_info'][0]['team_gold'] = blue_teamgold[index]
        video_dict['frames'][index]['data']['team_info'][1]['team_gold'] = red_teamgold[index]

        video_dict['frames'][index]['data']['team_info'][0]['tower_kill'] = blue_tower_score[index]
        video_dict['frames'][index]['data']['team_info'][1]['tower_kill'] = red_tower_score[index]


        video_dict['frames'][index]['data']['team_info'][0]['object_kill'] = list()
        video_dict['frames'][index]['data']['team_info'][1]['object_kill'] = list()
    
    
    for index in range(len(video_dict['frames'])):
        if (blue_drake[index] != 0 or red_drake[index] != 0):
            video_dict['frames'][index]['data']['team_info'][0]['object_kill'].append(blue_drake[index])
            video_dict['frames'][index]['data']['team_info'][1]['object_kill'].append(red_drake[index])
        if (blue_nashor_herald[index] == 'summon_herald' or red_nashor_herald[index] == 'summon_herald'):
            video_dict['frames'][index]['data']['team_info'][0]['object_kill'].append(blue_nashor_herald[index])
            video_dict['frames'][index]['data']['team_info'][1]['object_kill'].append(red_nashor_herald[index])
        if blue_nashor_herald[index] == 'nashor' or red_nashor_herald[index] == 'nashor' :
            video_dict['frames'][index]['data']['team_info'][0]['object_kill'].append(blue_nashor_herald[index])
            video_dict['frames'][index]['data']['team_info'][1]['object_kill'].append(red_nashor_herald[index])
            
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["level"]= blue_top_level[index]
        video_dict['frames'][index]['data']['participant_info'][1]["level"]= blue_jug_level[index]
        video_dict['frames'][index]['data']['participant_info'][2]["level"]= blue_mid_level[index]
        video_dict['frames'][index]['data']['participant_info'][3]["level"]= blue_bot_level[index]
        video_dict['frames'][index]['data']['participant_info'][4]["level"]= blue_sup_level[index]
        video_dict['frames'][index]['data']['participant_info'][5]["level"]= red_top_level[index]
        video_dict['frames'][index]['data']['participant_info'][6]["level"]= red_jug_level[index]
        video_dict['frames'][index]['data']['participant_info'][7]["level"]= red_mid_level[index]
        video_dict['frames'][index]['data']['participant_info'][8]["level"]= red_bot_level[index]
        video_dict['frames'][index]['data']['participant_info'][9]["level"]= red_sup_level[index]      
        
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["cs"]= blue_top_cs[index]
        video_dict['frames'][index]['data']['participant_info'][1]["cs"]= blue_jug_cs[index]
        video_dict['frames'][index]['data']['participant_info'][2]["cs"]= blue_mid_cs[index]
        video_dict['frames'][index]['data']['participant_info'][3]["cs"]= blue_bot_cs[index]
        video_dict['frames'][index]['data']['participant_info'][4]["cs"]= blue_sup_cs[index]
        video_dict['frames'][index]['data']['participant_info'][5]["cs"]= red_top_cs[index]
        video_dict['frames'][index]['data']['participant_info'][6]["cs"]= red_jug_cs[index]
        video_dict['frames'][index]['data']['participant_info'][7]["cs"]= red_mid_cs[index]
        video_dict['frames'][index]['data']['participant_info'][8]["cs"]= red_bot_cs[index]
        video_dict['frames'][index]['data']['participant_info'][9]["cs"]= red_sup_cs[index]
        
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["kill"]= blue_top_k[index]
        video_dict['frames'][index]['data']['participant_info'][1]["kill"]= blue_jug_k[index]
        video_dict['frames'][index]['data']['participant_info'][2]["kill"]= blue_mid_k[index]
        video_dict['frames'][index]['data']['participant_info'][3]["kill"]= blue_bot_k[index]
        video_dict['frames'][index]['data']['participant_info'][4]["kill"]= blue_sup_k[index]
        video_dict['frames'][index]['data']['participant_info'][5]["kill"]= red_top_k[index]
        video_dict['frames'][index]['data']['participant_info'][6]["kill"]= red_jug_k[index]
        video_dict['frames'][index]['data']['participant_info'][7]["kill"]= red_mid_k[index]
        video_dict['frames'][index]['data']['participant_info'][8]["kill"]= red_bot_k[index]
        video_dict['frames'][index]['data']['participant_info'][9]["kill"]= red_sup_k[index]
    
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["death"]= blue_top_d[index]
        video_dict['frames'][index]['data']['participant_info'][1]["death"]= blue_jug_d[index]
        video_dict['frames'][index]['data']['participant_info'][2]["death"]= blue_mid_d[index]
        video_dict['frames'][index]['data']['participant_info'][3]["death"]= blue_bot_d[index]
        video_dict['frames'][index]['data']['participant_info'][4]["death"]= blue_sup_d[index]
        video_dict['frames'][index]['data']['participant_info'][5]["death"]= red_top_d[index]
        video_dict['frames'][index]['data']['participant_info'][6]["death"]= red_jug_d[index]
        video_dict['frames'][index]['data']['participant_info'][7]["death"]= red_mid_d[index]
        video_dict['frames'][index]['data']['participant_info'][8]["death"]= red_bot_d[index]
        video_dict['frames'][index]['data']['participant_info'][9]["death"]= red_sup_d[index]
        
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["assists"]= blue_top_a[index]
        video_dict['frames'][index]['data']['participant_info'][1]["assists"]= blue_jug_a[index]
        video_dict['frames'][index]['data']['participant_info'][2]["assists"]= blue_mid_a[index]
        video_dict['frames'][index]['data']['participant_info'][3]["assists"]= blue_bot_a[index]
        video_dict['frames'][index]['data']['participant_info'][4]["assists"]= blue_sup_a[index]
        video_dict['frames'][index]['data']['participant_info'][5]["assists"]= red_top_a[index]
        video_dict['frames'][index]['data']['participant_info'][6]["assists"]= red_jug_a[index]
        video_dict['frames'][index]['data']['participant_info'][7]["assists"]= red_mid_a[index]
        video_dict['frames'][index]['data']['participant_info'][8]["assists"]= red_bot_a[index]
        video_dict['frames'][index]['data']['participant_info'][9]["assists"]= red_sup_a[index]
        
        
    for index in range(len(video_dict['frames'])):
        video_dict['frames'][index]['data']['participant_info'][0]["vision_score"]= blue_top_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][1]["vision_score"]= blue_jug_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][2]["vision_score"]= blue_mid_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][3]["vision_score"]= blue_bot_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][4]["vision_score"]= blue_sup_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][5]["vision_score"]= red_top_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][6]["vision_score"]= red_jug_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][7]["vision_score"]= red_mid_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][8]["vision_score"]= red_bot_vision_score[index]
        video_dict['frames'][index]['data']['participant_info'][9]["vision_score"]= red_sup_vision_score[index]
    
    for index in range(len(video_dict['frames'])):
        if killer[index] != 0 or victim[index] !=0 :
            video_dict['frames'][index]['data']['fight']['killer'] = killer[index]
            video_dict['frames'][index]['data']['fight']['victim'] = victim[index]
    
    static_info.update(video_dict)
    final_json_dict = static_info 
    
    return final_json_dict

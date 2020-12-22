import glob
import os

import pandas as pd
import numpy as np
import datetime

import src.constants as constants

def get_static_indicator(raw_df,df):
    raw_df = raw_df.copy()
    df = df.copy()
    cols = [
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

    df_dict={}

    for i in cols:
        if 'player' in i:
            raw_df[i[:i.rfind('_')+1]+'port'] = raw_df[i[:i.rfind('_')+1]+'port'].apply(lambda x: x[1:-1].split(','))

    for i in cols:
        if 'team' in i:
            df_dict[i] = raw_df[i[:i.rfind('_')+1]+'top_port'].str[0].str[1:-1]
        elif 'player' in i:
            if np.round(raw_df[i[:i.rfind('_')+1]+'port'].str.len().mean())<3:
                df_dict[i] = raw_df[i[:i.rfind('_')+1]+'port'].str[0].str[1:-1] 
            else:
                df_dict[i] = raw_df[i[:i.rfind('_')+1]+'port'].str[1].str[2:-1]   
    
    check_freq = pd.DataFrame(df_dict)
    static_dict = dict.fromkeys(cols,None)
    
    for i in cols:
        if 'blue' in i:
            if 'set_score' in i:
                static_dict[i] = int(raw_df[raw_df.blue_set_score.str.len()==8]['blue_set_score'].mode().iloc[0][5:6])
            elif 'drake' in i:
                static_dict[i] = df['blue_drake'].dropna().tolist()
            elif 'nashor' in i:
                static_dict[i] = df['blue_nashor_herald'].dropna().tolist().count('nashor')
            elif 'summon' in i:
                static_dict[i] = df['blue_nashor_herald'].dropna().tolist().count('summon_herald')
            else:
                static_dict[i] = check_freq[i].mode().iloc[0]
        if 'red' in i:
            if 'set_score' in i:
                static_dict[i] = int(raw_df[raw_df.red_set_score.str.len()==8]['red_set_score'].mode().iloc[0][2:3])
            elif 'drake' in i:
                static_dict[i] = df['red_drake'].dropna().tolist()
            elif 'nashor' in i:
                static_dict[i] = df['red_nashor_herald'].dropna().tolist().count('nashor')
            elif 'summon' in i:
                static_dict[i] = df['red_nashor_herald'].dropna().tolist().count('summon_herald')
            else:
                static_dict[i] = check_freq[i].mode().iloc[0]
                
    
    static_info_df_value = [[static_dict[i] for i in cols]]
    static_info_df = pd.DataFrame(static_info_df_value, columns = cols, index=['game'])
    return static_info_df

def team_indicator(df):
    new_dict=dict()
    new_dict['first_blood_killer'] = []
    new_dict['first_tower_team'] = []
    new_dict['red_tower_score'] = []
    new_dict['blue_tower_score'] = []
    new_dict['red_drake'] = []
    new_dict['blue_drake'] = []
    new_dict['red_herald_summon'] = []
    new_dict['blue_herald_summon'] = []
    new_dict['red_nashor'] = []
    new_dict['blue_nashor'] = []
    new_dict['red_drake'] = []
    new_dict['nashor_gold_diff'] = []
    # new_dict['red_inhibitor'] = []
    # new_dict['blue_inhibitor'] = []

    first_blood = df[df.sentence=='first_blood_sentence'][['red_top_k','red_jug_k','red_mid_k','red_bot_k','red_sup_k','blue_top_k','blue_jug_k','blue_mid_k','blue_bot_k','blue_sup_k']]

    for x in first_blood.columns:
        if first_blood[x].values == [1.0]:
            first_blood_killer = x
        else :
            first_blood_killer = np.nan

    nashor_df = df[df.sentence=='nashor_sentence'][['video_timestamp','blue_nashor_herald','red_nashor_herald','red_teamgold','blue_teamgold']]
    nashor_gold_diff = []

    for x in nashor_df[(nashor_df.red_nashor_herald=='nashor')|(nashor_df.blue_nashor_herald=='nashor')].index:
        temp_df = df.loc[x:x+180,['red_teamgold','blue_teamgold']].dropna()
        nashor_gold_diff.append(temp_df.iloc[-1,:].values[0] - temp_df.iloc[-1,:].values[1])

    new_dict['first_blood_killer'] += [first_blood_killer]
    new_dict['first_tower_team'] += [df[(df.sentence=='red_first_tower_sentence')|(df.sentence=='blue_first_tower_sentence')]['tower'].values[0]]
    new_dict['red_tower_score'] += [len(df[(df.tower=='Red')|(df.tower=='Red_First')])]
    new_dict['blue_tower_score'] += [len(df[(df.tower=='Blue')|(df.tower=='Blue_First')])]
    new_dict['red_drake'] += [len(df[df.sentence=='red_dragon_sentence'])]
    new_dict['blue_drake'] += [len(df[df.sentence=='blue_dragon_sentence'])]
    new_dict['red_herald_summon'] += [df[df.sentence=='herald_summon_sentence']['red_nashor_herald'].count()]
    new_dict['blue_herald_summon'] += [df[df.sentence=='herald_summon_sentence']['blue_nashor_herald'].count()]
    new_dict['red_nashor'] += [len(nashor_df[nashor_df.red_nashor_herald=='nashor'])]
    new_dict['blue_nashor'] += [len(nashor_df[nashor_df.blue_nashor_herald=='nashor'])]
    new_dict['nashor_gold_diff'] += [np.array(nashor_gold_diff).round(2)]

    indicator_df = pd.DataFrame(new_dict, index=['game'])

    return indicator_df


def get_df_under15(df) :
    df = df.copy()
    def to_time(x) :
        try :
            return datetime.datetime.strptime(x[0:5],'%M:%S').second + (datetime.datetime.strptime(x[0:5],'%M:%S').minute)*60
        except :
            return np.nan

    df['timestamp'] = df.timestamp.apply(lambda x : to_time(x))

    positions=['top','jug','mid','bot','sup']
    for pos in positions :
        df[f"blue_{pos}_level"] = df[f"blue_{pos}_level"].values
        df[f"red_{pos}_level"] = df[f"red_{pos}_level"].values

        df[f"{pos}_level_gap"] = df[f"blue_{pos}_level"] - df[f"red_{pos}_level"]
        df[f"{pos}_cs_gap"] = df[f"blue_{pos}_cs"] - df[f"red_{pos}_cs"]

#        df[f"{pos}_level_gap"] = df[f"{pos}_level_gap"].interpolate()
        df[f"{pos}_cs_gap"] = df[f"{pos}_cs_gap"].interpolate()
        
    df_under15 = df[df["timestamp"]<=900]

    return df_under15

def get_df_end(df) :
    df = df.copy()
    def to_time(x) :
        try :
            return datetime.datetime.strptime(x[0:5],'%M:%S').second + (datetime.datetime.strptime(x[0:5],'%M:%S').minute)*60
        except :
            return np.nan

    df['timestamp'] = df.timestamp.apply(lambda x : to_time(x))

    df = df[-300:]
    return df

def make_player_indicator_under15(df_use) :
    new_dict=dict()
    positions=['top','jug','mid','bot','sup']
    minutes = [9,15]
    for pos in positions :
        for m in minutes:
            try :
                new_dict[f"{pos}_cs_gap_{m}m"]=int(df_use[df_use['timestamp']==m*60][f"{pos}_cs_gap"].values[0])
            except :
                try :
                    new_dict[f"{pos}_cs_gap_{m}m"]=int(df_use[df_use['timestamp']==(m*60-10)][f"{pos}_cs_gap"].values[0]+df_use[df_use['timestamp']==(m*60+10)][f"{pos}_cs_gap"].values[0])/2                
                except :
                    new_dict[f"{pos}_cs_gap_{m}m"]=np.nan

    for pos in positions :
        for m in minutes:
            try :
                new_dict[f"{pos}_level_gap_{m}m"]=int(df_use[df_use['timestamp']==m*60][f"{pos}_level_gap"].values[0])
            except :
                try :
                    new_dict[f"{pos}_level_gap_{m}m"]=int(df_use[df_use['timestamp']==(m*60-10)][f"{pos}_level_gap"].values[0]+df_use[df_use['timestamp']==(m*60+10)][f"{pos}_level_gap"].values[0])/2                
                except :
                    new_dict[f"{pos}_level_gap_{m}m"]=np.nan
    
    return pd.DataFrame(new_dict, index=['game'])

def make_player_indicator_end(df_use) :
    new_dict=dict()
    positions=['top','jug','mid','bot','sup']
    for side in ['blue','red'] :
        for pos in positions :
            col = f"{side}_{pos}_cs"
            i_cs = df_use[col].last_valid_index()
            new_dict[f"{side}_{pos}_cspm_final"] = df_use[col].loc[i_cs]/df_use["timestamp"].loc[i_cs]*60

    cols = [f"{side}_{pos}_{val}" for side in ['blue','red'] for pos in positions for val in ['k','d','a']]
    df_use = df_use[cols].dropna(how='any')
    for side in ['blue','red'] :
        total_kill = 0
        total_death = 0
        for pos in positions :
            k = df_use[f"{side}_{pos}_k"].iloc[-1]
            new_dict[f"{side}_{pos}_k_final"] = k
            d = df_use[f"{side}_{pos}_d"].iloc[-1]
            new_dict[f"{side}_{pos}_d_final"] = d
            a = df_use[f"{side}_{pos}_a"].iloc[-1]
            new_dict[f"{side}_{pos}_a_final"] = a
            try :
                if d != 0 :
                    new_dict[f"{side}_{pos}_kda_final"] = (k+a)/d
                else :
                    new_dict[f"{side}_{pos}_kda_final"] = -1          # perfect kda -> -1
            except :
                new_dict[f"{side}_{pos}_kda_final"] = np.nan

            total_kill += k
            total_death += d

        for pos in positions :
            k = df_use[f"{side}_{pos}_k"].iloc[-1]
            d = df_use[f"{side}_{pos}_d"].iloc[-1]
            a = df_use[f"{side}_{pos}_a"].iloc[-1]
            if total_kill != 0 :
                new_dict[f"{side}_{pos}_killparticip_final"] = (k+a)/total_kill
            else :
                new_dict[f"{side}_{pos}_killparticip_final"] = 0            
            if total_death != 0 :
                new_dict[f"{side}_{pos}_deathparticip_final"] = d/total_death
            else :
                new_dict[f"{side}_{pos}_deathparticip_final"] = 0

    return pd.DataFrame(new_dict, index=['game'])

def run(video):
    raw_df = pd.read_csv(constants.CSV_PATH + "\\raw_" + video + ".csv")
    df = pd.read_csv(constants.CSV_PATH + "\\" + video + ".csv")
    
    row_static = get_static_indicator(raw_df,df)
    row_team = team_indicator(df)
    row_player_end = make_player_indicator_end(get_df_end(df))
    row_player_under15 = make_player_indicator_end(get_df_under15(df))
    
    row_total = pd.concat([row_static, row_team, row_player_end, row_player_under15], axis=1)
    row_total['video_name'] = video
    row_total.set_index('video_name')

    return row_total
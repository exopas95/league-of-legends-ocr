import numpy as np
import pandas as pd
import re


""" Returns [kill, death, assist] if input word can be decrypted else nan
    - param x: Input word will define which is kda or not
    - type x: str
"""
def judge_kda(x) :
    try :
        if np.isnan(x) :
            return x
    except :
        word = re.sub(r'[^0-9/]', '', x)            # These are only characters required

        n_slash = 0
        n_seven = 0                                 # Vision reads '/' to '7' usually
        seven_index = []
        for i, char in enumerate(word) :
            if (char == '/') :
                n_slash += 1
            elif (char == '7') :
                n_seven += 1
                seven_index.append(i)

        if n_slash == 2 :                           # Best case
            kda = re.split('/', word)

        else :
            if (n_seven == 1) & (n_slash == 1) :    # '7' can be '/' or real value, but if there are only one '7', no other possibilities
                kda = re.split('/|7', word)

            else :
                rep = (('77', 'a/'), ('7/', 'a/'), ('777', '/a/'), ('7777', 'a/a/'))        # Assume there are no possibilities to obtain 70+ k,d,a
                for r in reversed(rep) :
                    word = word.replace(*r)
                kda = re.split('/|7', word)
                kda = list(filter(lambda x: x != '', kda))                                  # Make values not empty
                if len(word)-1 in seven_index :                                             # Push 7 for remain possibilities (e.g.7/0/7) 
                    kda[-1] += '7'

        kda = [re.sub('a', '7', x) for x in kda]    # substitute 'a' to '7'

        if len(kda) == 3 :                          # If it splited well, length of list should be 3
            try :
                kda = [int(x) for x in kda]
                return kda
            except :
                return np.nan
        else :
            return np.nan

""" Find a value of level where portraits are masked with '999'
     - param x: A list contains characters from portrait
     - type x: list

     - param side: 'blue' or 'red'
     - type side: str
"""
def judge_level(x, side) :
    try :
        if np.isnan(x) :
            return x
    except :
        word = ''.join(x)
        try :
            if bool(re.search('9999', word)) :
                return int(9)
            else :
                startend_points = re.search(r'999', word).span()
                if side == 'red' :
                    i = startend_points[0]
                    level_candidate = word[max(0,i-2):i]
                elif side == 'blue' :
                    i = startend_points[1]
                    level_candidate = word[i:min(i+2,len(word))]                        
                level = re.sub(r'[^0-9]', '', level_candidate)
                return int(level)
        except :
            return np.nan


""" Make a monotonic increasing sequence from the left
    - param a: Input array try to make monotonic
    - type a: list
    
    - param ths: To determine the value that bounces up, 
        a threshold that determines how many values have gone down after bouncing up
    - type ths: int
"""
def make_inc(a, ths) :
    a_inc = []
    i = 0
    temp = 0
    coin = 0
    while i < len(a) :
        if np.isnan(a[i]) :
            a_inc.append(np.nan)
            i += 1
        else :
            if (a[i] >= temp) & (a[i]<1000) :       # Check if value is increasing
                a_inc.append(a[i])                  # Assume there is no possibility to cs exceed 1000
                temp = a[i]
                i += 1
            else :
                if coin > ths :                     # If value continues to be below, 
                    i -= ths                        # think that the corresponding temp is the bouncing up value 
                    coin = 0                        # and go back and save it as nan
                    temp = a[i-1]                   # and place the previous value as temp
                    a_inc = a_inc[:-(ths+2)]
                    a_inc.append(np.nan)
                    a_inc.append(a[i-1])
                else :                              
                    a_inc.append(np.nan)            # For the moment consider it as a bouncing value and save nan
                    i += 1                          
                    coin += 1                       
    return a_inc

""" Make a monotonic decreasing sequence from the right
    - param a: Input array try to make monotonic
    - type a: list
    
    - param ths: Determines how many values have gone down after bouncing down
    - type ths: int
"""
def make_dec(a, ths) :
    a_temp = []
    i = len(a)-1                                    # Start from back
    temp = 0
    coin = 0
    while i >= 0 :
        if np.isnan(a[i]) :
            a_temp.append(np.nan)
            i -= 1
        else :
            if (a[i] <= temp) & (a[i]<1000) :       # Check if value is decreasing
                a_temp.append(a[i])
                temp = a[i]
                i -= 1
            else :
                if coin > ths :
                    i += ths
                    coin = 0
                    temp = a[i+1]
                    a_temp = a_temp[:-(ths+2)]
                    a_temp.append(np.nan)
                    a_temp.append(a[i+1])
                else :
                    a_temp.append(np.nan)
                    i -= 1
                    coin += 1
    
    a_dec = [x for x in reversed(a_temp)]           # Reverse outcome list
    return a_dec


""" Join two pseudo-monotonic array as one
    - param a: Input array try to make monotonic
    - type a: list
    
    - param ths: Determines how many values have gone down after bouncing up or down
    - type ths: int
"""
def make_monotonic(a, ths) :
    a_mono = []
    for x,y in zip(make_dec(a, ths), make_inc(a, ths)) :
        if x == y :                                 # If the two functions do not produce the same value, 
            a_mono.append(x)                        # determine that there is an error and receive a nan
        else :
            a_mono.append(np.nan)
    return a_mono

""" Remove before and after of the game and remain the start to the end of game with timestamp
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_game_df(df) :
    df['timestamp'] = df['timestamp'].apply(lambda x: np.nan if len(x)==0 else x)   # Replace empty list into nan
    timestamps = df.dropna(subset=['timestamp']).index                              # get index of rows with timestamp
    return df.loc[timestamps[0]:timestamps[-1]]                                     # Get remain of the start to the end of a game


""" Get list of timestamp as string from input dataframe 
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_timestamp(df) : 
    l = []
    for x in df.timestamp.values :
        try :
            if bool(re.match(r'[\d\d]+:[\d\d]+', x[0])) :           # Find only the value that fits the form 'dd:dd' or nan 
                l.append(x[0])
            else :
                l.append(np.nan)
        except :
            l.append(x)
    return l


""" Get list of teamgold aligned by timestamp as float from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe

    - param side: 'red' or 'blue' 
    - type side: str
"""
def get_teamgold(df, side) :
    l = []
    def isgold(l, side) :           # Internal method to assert value represents gold
        s = np.nan
        if side =='blue' :
            l = reversed(l)
        elif side == 'red' :
            l = l            
        for x in l :
            if len(x) > 3 :         # There are noise texts while reading team gold location('c', 'C', 'G', etc.) 
                s = x               # If team gold read well, the length is over four.(e.g.len('2.5k')=4)
                break
            else :
                continue
        return s

    for x in df[side+'_teamgold'].values :
        try :
            raw_gold = isgold(x, side)
            gold = float(re.sub(',', '.', re.sub(r'[^0-9.,]', '', raw_gold)))       # Decimal point can be read as comma, so replace it
            l.append(gold)                                                          # with only period and digits,
        except :                                                                    # gold can be easily converted to float
            l.append(np.nan)
    return make_monotonic(l, 5)                                                     # team gold is monotonically increasing


""" Get list of cs aligned by timestamp as float from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe

    - param side: 'red' or 'blue' 
    - type side: str

    - param pos: 'top' / 'jug' / 'mid' / 'bot' / 'sup' 
    - type pos: str
"""
def get_cs(df, side, pos) :
    l = []
    for x in df[side+'_'+pos+'_cs'].values :
        if len(x) > 0 :
            try :                                   # Assume the value is one and only
                l.append(float(x[0]))
            except :
                l.append(np.nan)
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)                     # cs is monotonically increasing


""" Get list of kda aligned by timestamp as float from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe

    - param side: 'red' or 'blue' 
    - type side: str

    - param pos: 'top' / 'jug' / 'mid' / 'bot' / 'sup' 
    - type pos: str

    - param kda: 'k' / 'd' / 'a' 
    - type pos: str
"""
def get_kda(df, side, pos, kda) :
    l=[]
    if kda == 'k' :
        kda_index = 0
    elif kda == 'd' :
        kda_index = 1
    elif kda == 'a' :
        kda_index = 2
    for x in df[side+'_'+pos+'_kda'].values :
        if len(x) > 0 :
            try :
                l.append(judge_kda(x[0])[kda_index])         # Use Method judge_kda, which is on the top of this file 
            except :                                        # judge_kda returns value with form of [kill, death, assist]
                l.append(np.nan)
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)                             # kda is monotonically increasing


""" Get tuple of list of notices(blue, red) from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_notice(df) :                                # Hard coded
    blue = []                                       # Need to add bag of words contains possible typing errors
    red = []
    for x in df['notice'].values :
        if len(x)>0 :
            if '파랑' in x :
                if '남작' in x :
                    red.append(np.nan)
                    blue.append('nashor')
                elif '드래곤' in x :
                    red.append(np.nan)
                    blue.append('drake')
                elif ('포탑' in x) :                # Turret will be recorded based on the team that breaks
                    if '번째' in x :                # Announce notices perpetrator for the first turret
                        blue.append('turret')       # (e.g.'파랑 팀이 첫 번째 포탑을 파괴했습니다')
                        red.append(np.nan)
                    else :
                        red.append('turret')        # Announce notices victim for other cases
                        blue.append(np.nan)         # (e.g. '빨강 팀의 포탑이 파괴되었습니다')
                else :
                    red.append(np.nan)
                    blue.append('unknown')          # Now, record 'unknown' when there are typing errors
            elif '빨강' in x :
                if '남작' in x :
                    blue.append(np.nan)
                    red.append('nashor')
                elif '드래곤' in x :
                    blue.append(np.nan)
                    red.append('drake')
                elif ('포탑' in x) :
                    if '번째' in x :
                        blue.append(np.nan)
                        red.append('turret')
                    else :
                        blue.append('turret')
                        red.append(np.nan)
                else :
                    blue.append(np.nan)
                    red.append('unknown')
            else :
                blue.append(np.nan)
                red.append(np.nan)
        else :
            blue.append(np.nan)
            red.append(np.nan)
    return blue, red                                # Return tuple, will be changed

""" Get list of level aligned by timestamp as float from input dataframe
     - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
     - type df: dataframe

     - param side: 'red' or 'blue' 
     - type side: str

     - param pos: 'top' / 'jug' / 'mid' / 'bot' / 'sup' 
     - type pos: str
"""
def get_level(df, side, pos) :
    l=[]
    for x in df[side+'_'+pos+'_port'].values :
        if len(x) > 0 :
            l.append(judge_level(x,side))
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)


def get_shutdown(df, side, pos) :

    def slash_count(x) :
        try :
            if np.isnan(x) :
                return 0
        except :
            n_slash = 0
            for i, char in enumerate(x) :
                if (char == '/') | (char=='7') :
                    n_slash += 1
        return n_slash

    def findgold(text) :
        try :
            tmp = text.split("'")
            for char in tmp :
                try :
                    if len(char) >= 3 :
                        cnt = slash_count(char)
                        if cnt < 2 :
                            char = ''.join(filter(str.isnumeric, char))
                            return char[-3:]
                except :
                    continue
        except :
            return np.nan
        return np.nan

    gold = []

    for text in df[side+'_'+pos+'_kda'] :
        gold.append(findgold(text))

    return gold
    
def get_vision_score(df, side, pos) :
    l=[]
    for x in df[side+'_'+pos+'_vision_score'].values :
        if len(x) > 0 :
            l.append(judge_level(x,side))
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)


def get_tower_score(df, side) :
    l=[]
    for x in df[side+'_tower_score'].values :
        if len(x) > 0 :
            l.append(judge_level(x,side))
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)

def get_set_score(df, side) :
    l=[]
    for x in df[side+'_set_score'].values :
        if len(x) > 0 :
            l.append(judge_level(x,side))
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)


""" Make new dataframe with pre-processed values
    Returns dataframe with columns of timestamp for a game, team gold, notice for each team, cs, kill, death, assist, for each team and lane
    Set index as timestamp
    When index is nan, there could be replay
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def result_process(df) :
    game_df = get_game_df(df)
    processed_df = pd.DataFrame({'timestamp' : get_timestamp(game_df),

                                'red_teamgold' : get_teamgold(game_df, 'red'),

                                'red_top_level' : get_level(game_df, 'red', 'top'),
                                'red_jug_level' : get_level(game_df, 'red', 'jug'),
                                'red_mid_level' : get_level(game_df, 'red', 'mid'),
                                'red_bot_level' : get_level(game_df, 'red', 'bot'),
                                'red_sup_level' : get_level(game_df, 'red', 'sup'),

                                'red_top_cs' : get_cs(game_df, 'red', 'top'),
                                'red_top_shutdown' : get_shutdown(game_df, 'red', 'top'),
                                'red_top_k' : get_kda(game_df, 'red', 'top', 'k'),
                                'red_top_d' : get_kda(game_df, 'red', 'top', 'd'),
                                'red_top_a' : get_kda(game_df, 'red', 'top', 'a'),

                                'red_jug_cs' : get_cs(game_df, 'red', 'jug'),
                                'red_jug_shutdown' : get_shutdown(game_df, 'red', 'jug'),
                                'red_jug_k' : get_kda(game_df, 'red', 'jug', 'k'),
                                'red_jug_d' : get_kda(game_df, 'red', 'jug', 'd'),
                                'red_jug_a' : get_kda(game_df, 'red', 'jug', 'a'),

                                'red_mid_cs' : get_cs(game_df, 'red', 'mid'),
                                'red_mid_shutdown' : get_shutdown(game_df, 'red', 'mid'),
                                'red_mid_k' : get_kda(game_df, 'red', 'mid', 'k'),
                                'red_mid_d' : get_kda(game_df, 'red', 'mid', 'd'),
                                'red_mid_a' : get_kda(game_df, 'red', 'mid', 'a'),

                                'red_bot_cs' : get_cs(game_df, 'red', 'bot'),
                                'red_bot_shutdown' : get_shutdown(game_df, 'red', 'bot'),
                                'red_bot_k' : get_kda(game_df, 'red', 'bot', 'k'),
                                'red_bot_d' : get_kda(game_df, 'red', 'bot', 'd'),
                                'red_bot_a' : get_kda(game_df, 'red', 'bot', 'a'),

                                'red_sup_cs' : get_cs(game_df, 'red', 'sup'),
                                'red_sup_shutdown' : get_shutdown(game_df, 'red', 'sup'),
                                'red_sup_k' : get_kda(game_df, 'red', 'sup', 'k'),
                                'red_sup_d' : get_kda(game_df, 'red', 'sup', 'd'),
                                'red_sup_a' : get_kda(game_df, 'red', 'sup', 'a'),

                                'red_notice' : get_notice(game_df)[0],

                                'blue_teamgold' : get_teamgold(game_df, 'blue'),

                                'blue_top_level' : get_level(game_df, 'blue', 'top'),
                                'blue_jug_level' : get_level(game_df, 'blue', 'jug'),
                                'blue_mid_level' : get_level(game_df, 'blue', 'mid'),
                                'blue_bot_level' : get_level(game_df, 'blue', 'bot'),
                                'blue_sup_level' : get_level(game_df, 'blue', 'sup'),

                                'blue_top_cs' : get_cs(game_df, 'blue', 'top'),
                                'blue_top_shutdown' : get_shutdown(game_df, 'blue', 'top'),
                                'blue_top_k' : get_kda(game_df, 'blue', 'top', 'k'),
                                'blue_top_d' : get_kda(game_df, 'blue', 'top', 'd'),
                                'blue_top_a' : get_kda(game_df, 'blue', 'top', 'a'),

                                'blue_jug_cs' : get_cs(game_df, 'blue', 'jug'),
                                'blue_jug_shutdown' : get_shutdown(game_df, 'blue', 'jug'),
                                'blue_jug_k' : get_kda(game_df, 'blue', 'jug', 'k'),
                                'blue_jug_d' : get_kda(game_df, 'blue', 'jug', 'd'),
                                'blue_jug_a' : get_kda(game_df, 'blue', 'jug', 'a'),

                                'blue_mid_cs' : get_cs(game_df, 'blue', 'mid'),
                                'blue_mid_shutdown' : get_shutdown(game_df, 'blue', 'mid'),
                                'blue_mid_k' : get_kda(game_df, 'blue', 'mid', 'k'),
                                'blue_mid_d' : get_kda(game_df, 'blue', 'mid', 'd'),
                                'blue_mid_a' : get_kda(game_df, 'blue', 'mid', 'a'),

                                'blue_bot_cs' : get_cs(game_df, 'blue', 'bot'),
                                'blue_bot_shutdown' : get_shutdown(game_df, 'blue', 'bot'),
                                'blue_bot_k' : get_kda(game_df, 'blue', 'bot', 'k'),
                                'blue_bot_d' : get_kda(game_df, 'blue', 'bot', 'd'),
                                'blue_bot_a' : get_kda(game_df, 'blue', 'bot', 'a'),

                                'blue_sup_cs' : get_cs(game_df, 'blue', 'sup'),
                                'blue_sup_shutdown' : get_shutdown(game_df, 'blue', 'sup'),
                                'blue_sup_k' : get_kda(game_df, 'blue', 'sup', 'k'),
                                'blue_sup_d' : get_kda(game_df, 'blue', 'sup', 'd'),
                                'blue_sup_a' : get_kda(game_df, 'blue', 'sup', 'a'),
                                
                                'blue_top_vision_score' : get_vision_score(game_df,'blue','top'),
                                'blue_jug_vision_score' : get_vision_score(game_df,'blue','jug'),
                                'blue_mid_vision_score' : get_vision_score(game_df,'blue','mid'),
                                'blue_bot_vision_score' : get_vision_score(game_df,'blue','bot'),
                                'blue_sup_vision_score' : get_vision_score(game_df,'blue','sup'),
                                
                                'red_top_vision_score' : get_vision_score(game_df,'red','top'),
                                'red_jug_vision_score' : get_vision_score(game_df,'red','jug'),
                                'red_mid_vision_score' : get_vision_score(game_df,'red','mid'),
                                'red_bot_vision_score' : get_vision_score(game_df,'red','bot'),
                                'red_sup_vision_score' : get_vision_score(game_df,'red','sup'),
                                
                                'blue_tower_score' : get_tower_score(game_df,'blue'),
                                'red_tower_score' : get_tower_score(game_df, 'red'),
                                
                                'blue_set_score' : get_set_score(game_df,'blue'),
                                'red_set_score' : get_set_score(game_df,'red'),
                                
                                'blue_notice' : get_notice(game_df)[1]}).set_index('timestamp')
                                
                                
                                
    return processed_df
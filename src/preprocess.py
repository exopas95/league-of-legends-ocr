import numpy as np
import pandas as pd
import time
import re
import math


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
    temp = 99999
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

def get_video_timestamp(df):
    df['video_timestamp'] = df['video_timestamp'].apply(lambda x: np.nan if len(x)==0 else time.strftime("%M:%S", time.gmtime(float(x))))   # Replace empty list into nan
    return df["video_timestamp"]
    
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

"""Deduplicate data from list for arrange notice
    - param data: Once-processed dataframe (has multiple-read in 'notice') 
    - type data: dataframe
"""

def df_target(df, keyword):
    target_index = []
    for x in df.index:
        if keyword in df.notice.loc[x]:
            target_index.append(x)
    return df.loc[target_index, :]

def deduplicate(df):
    dedup_index = []
    for i in df.index:
        if len(dedup_index) == 0:
            dedup_index.append(i)
        else:
            if int(dedup_index[-1].split('_')[-1])+4 < int(i.split('_')[-1]):
                dedup_index.append(i)
    return df.loc[dedup_index, :]

""" Get tuple of list of drake/dragon(blue, red) from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_drake(df) :
    seq = []
    drake_type = ['INFERNAL', 'CLOUD', 'MOUNTAIN', 'OCEAN']
    for x in df['left_top_dragon_info'].values :
        for y in drake_type:
            if (y in x) and (y not in seq) :
                seq.append(y)
    df_drake_pre = df_target(df, '드래곤')
    df_drake = deduplicate(df_drake_pre)
    blue = []
    red = []
    blue_dra_stack = 0
    red_dra_stack = 0
    has_error = ''
    total_stack = blue_dra_stack + red_dra_stack
    for x in df.index :
        if x in df_drake.index:
            if '드래곤' in df.notice.loc[x] :
                if '파랑' in df.notice.loc[x] :
                    blue_dra_stack += 1
                    red.append(np.nan)
                    total_stack = blue_dra_stack + red_dra_stack
                    if total_stack < 3:
                        blue.append(has_error+seq[total_stack-1]+'DRAKE')
                        print(seq[total_stack-1])
                    elif total_stack >= 3:
                        if (blue_dra_stack > 4) or (red_dra_stack >= 4):      #red got 4 dragon or blue already got 4 dragon 
                            blue.append(has_error+'ELDER'+'DRAKE')
                        else:
                            blue.append(has_error+seq[2]+'DRAKE')
                            print(seq[2])
                elif '빨강' in df.notice.loc[x] :
                    red_dra_stack += 1
                    blue.append(np.nan)
                    total_stack = blue_dra_stack + red_dra_stack
                    if total_stack < 3:
                        red.append(has_error+seq[total_stack-1]+'DRAKE')
                    elif total_stack >= 3:
                        if (red_dra_stack > 4) or (blue_dra_stack >= 4):
                            red.append(has_error+'ELDER'+'DRAKE')
                        else:
                            red.append(has_error+seq[2]+'DRAKE')
                else:                                         #slain drake but don't know team
                    red.append('UNKNOWN'+'DRAKE')
                    blue.append('UNKNOWN'+'DRAKE')
                    has_error = '[ERROR]'
            else:
                red.append(np.nan)
                blue.append(np.nan)
        else:
            red.append(np.nan)
            blue.append(np.nan)
    return blue, red

""" Get tuple of list of nashor/herald(blue, red) from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_nashor_herald(df) :
    blue = []
    red = []
    df_nashor_pre = df_target(df, '내셔')
    df_herald_pre = df_target(df, '전령')
    df_nashor = deduplicate(df_nashor_pre)
    df_herald = deduplicate(df_herald_pre)
    df_object = pd.concat([df_nashor, df_herald])
    for x in df.index :
        if x in df_object.index :
            if '파랑' in df.notice.loc[x] :
                if '남작' in df.notice.loc[x] :
                    red.append(np.nan)
                    blue.append('nashor')
                elif '전령' in df.notice.loc[x] :
                    red.append(np.nan)
                    blue.append('summon_herald')
                else:
                    red.append(np.nan)
                    blue.append(np.nan)
            elif '빨강' in df.notice.loc[x] :
                if '남작' in df.notice.loc[x] :
                    blue.append(np.nan)
                    red.append('nashor')
                elif '전령' in df.notice.loc[x] :
                    blue.append(np.nan)
                    red.append('summon_herald')
                else:
                    red.append(np.nan)
                    blue.append(np.nan)
            else:
                blue.append(np.nan)
                red.append(np.nan)
        else:
            blue.append(np.nan)
            red.append(np.nan)
        
    return blue, red

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
    return l

def valid_vision_score(l):
    include_nan = []
    except_nan = []
    for x in l:
        if math.isnan(x):
            include_nan.append(np.nan)
        else:
            y = int(x)
            if len(except_nan) == 0:
                include_nan.append(y)
                except_nan.append(y)
            else:
                if y > except_nan[-1]:
                    if len(str(y)) > len(str(except_nan[-1])):
                        if (str(y)[-1] == '1') or (str(y)[-1] == '2'):
                            if (y > except_nan[-1] + 9):
                                include_nan.append(int(str(y)[:-1]))
                                except_nan.append(int(str(y)[:-1]))
                            else:
                                include_nan.append(y)
                                except_nan.append(y)
                        elif (str(y)[0] == '7') or (str(y)[0] == '2'):
                            if (y > except_nan[-1] + 9):
                                include_nan.append(int(str(y)[1:]))
                                except_nan.append(int(str(y)[1:])) 
                            else:
                                include_nan.append(y)
                                except_nan.append(y)
                        else:
                            include_nan.append(y)
                            except_nan.append(y)
                    else:
                        include_nan.append(y)
                        except_nan.append(y)
                elif y == except_nan[-1]:
                    include_nan.append(y)
                    except_nan.append(y)                    
                else:
                    include_nan.append(np.nan)
    return include_nan


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

# main text
total_sentence = {
    'start_sentence' : '소환사의협곡에오신것을환영합니다',
    'minion_30_sentence' : '미니언생성까지초남았습니다',
    'minion_sentence' : '미니언이생성 되었습니다',
    'first_blood_sentence' : '선취점',
    'kill_sentence0' : '님이님을처치했습니다',
    'kill_sentence1' : '님이학살중입니다',
    'kill_sentence2' : '님을도저히막을수없습니다',
    'kill_sentence3' : '연속킬차단',
    'kill_sentence4' : '님이미쳐날뛰고있습니다',
    'kill_sentence5' :  '마지막적처치',
    'kill_sentence6' : '더블킬',
    'kill_sentence7' : '트리플킬',
    'kill_sentence8' : '쿼드라킬',
    'kill_sentence9' : '펜타킬',
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
    'sumi_sentence' : '님이팀억제기를파괴했습니다'
    }

text_str = ['start_sentence', 'minion_30_sentence', 'minion_sentence', 'first_blood_sentence',
            'kill_sentence0', 'kill_sentence1', 'kill_sentence2', 'kill_sentence3', 'kill_sentence4',
            'kill_sentence5', 'kill_sentence6', 'kill_sentence7', 'kill_sentence8', 'kill_sentence9',
            'red_dragon_sentence', 'blue_dragon_sentence', 'blue_tower_sentence',
            'red_tower_sentence', 'blue_first_tower_sentence', 'red_first_tower_sentence',
            'herald_summon_sentence', 'nashor_sentence', 'sumi_sentence']




def get_sentence(df) :

    def list_to_str(x) :
        result = re.compile('[가-힣a-zA-Z]+').findall(x)
        if result :
            result = ''.join(result)
        else :
            result = np.nan
        return result

    def notice_cleaner(df) :
        text = df.notice.apply(
            lambda x : list_to_str(x)
        )
        return text

    def calculator_similar(x,y) :
        cnt = 0
        try :
            for x_char in x:
                for y_char in y :
                    if x_char == y_char :
                        cnt += 1
        except :
            cnt = 0
        return cnt/len(y)

    def get_index(x) :
        if max(x) <= 0.65 :
            return np.nan
        return x.astype(float).idxmax()


    similar = pd.DataFrame(columns=['text']+text_str)
    similar['text'] = notice_cleaner(df)
    
    for i in text_str :
        similar[i] = similar.text.apply(
            lambda x : calculator_similar(x,total_sentence[i])
        )

    real_text = []
    max_cnt = []
    similar_T = similar.T
    for i in range(len(similar)) :
        real_text.append(get_index((similar_T)[i][1:]))
        max_cnt.append((similar_T)[i][1:].max())

    similar['real_text'] = real_text
    similar['max_cnt'] = max_cnt
    
    sentence = similar.real_text.copy().fillna("0")

    tmp = sentence.iloc[0]
    tmp_idx = sentence.index[0]
    for i in sentence.index[1:] :
        if 'tower' in tmp :
            if (i - tmp_idx < 5) & (sentence[i] == tmp) :
                sentence[i] = 'DUP'
            else :
                tmp = sentence[i]
                tmp_idx = i
        else :
            if (i - tmp_idx < 3) & (sentence[i] == tmp) :
                sentence[i] = 'DUP'
            else :
                tmp = sentence[i]
                tmp_idx = i    
    sentence = sentence.replace("0","DUP")

    return sentence

def get_kill(df) :
    df['sentence'] = get_sentence(df)
    def killer_victim_find(x) :
        n_sub = 0
        for char in x :
            if (char == "임") | (char=='님') :
                n_sub += 1
        if n_sub == 0 :
            return 'IDK', 'IDK'
        
        if n_sub == 1 :
            if '님' in x :
                return x[x.index("님")-1], 'IDK'
            else :
                return x[x.index('임')-1], 'IDK'
        if n_sub >= 2 :
            try :
                a = x.index("님")
            except :
                a = 100
            try :
                b = x.index("임")
            except :
                b = 100
            re1 = min(a,b)

            rev = list(reversed(x))
            try :
                a = rev.index("님")
            except :
                a = 100
            try :
                b = rev.index("임")
            except :
                b = 100
            re2 = min(a,b)
            return x[re1-1], rev[re2+1]
        return 'IDK', 'IDK'



    killer, victim = [], []
    for x in df.index :
        if 'blood' in df.sentence[x] :
            killer.append( 'IDK' )
            victim.append( 'IDK' )
        elif 'kill' in df.sentence[x] :
            cleaned_x = re.compile('[가-힣a-zA-Z0-9]+').findall(df.notice[x])
            ki, vi = killer_victim_find(cleaned_x)
            killer.append(ki)
            victim.append(vi)
        else :
            killer.append(np.nan)
            victim.append(np.nan)
    return killer, victim

def get_tower(df) :
    df['sentence'] = get_sentence(df)
    def tower(sent) :
        if 'blue_first' in sent :
            return ("Blue_First")
        if 'red_first' in sent :
            return ("Red_First")
        if 'blue_tower' in sent :
            return ("Blue")
        if 'red_tower' in sent :
            return ("Red")
        else :
            return ("None")

    result = df.sentence.apply(
        lambda x : tower(x)
    )
    return result







""" Make new dataframe with pre-processed values
    Returns dataframe with columns of timestamp for a game, team gold, notice for each team, cs, kill, death, assist, for each team and lane
    Set index as timestamp
    When index is nan, there could be replay
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def result_process(df) :
    game_df = get_game_df(df)
    processed_df = pd.DataFrame({"video_timestamp": get_video_timestamp(game_df),
                                'timestamp' : get_timestamp(game_df),
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
                                
                                'blue_top_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','top')),
                                'blue_jug_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','jug')),
                                'blue_mid_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','mid')),
                                'blue_bot_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','bot')),
                                'blue_sup_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','sup')),
                                
                                'red_top_vision_score' : valid_vision_score(get_vision_score(game_df,'red','top')),
                                'red_jug_vision_score' : valid_vision_score(get_vision_score(game_df,'red','jug')),
                                'red_mid_vision_score' : valid_vision_score(get_vision_score(game_df,'red','mid')),
                                'red_bot_vision_score' : valid_vision_score(get_vision_score(game_df,'red','bot')),
                                'red_sup_vision_score' : valid_vision_score(get_vision_score(game_df,'red','sup')),
                                
                                'blue_tower_score' : get_tower_score(game_df,'blue'),
                                'red_tower_score' : get_tower_score(game_df, 'red'),

                                'blue_drake' : get_drake(game_df)[0],
                                'blue_nashor_herald' : get_nashor_herald(game_df)[0],
                                'red_drake' : get_drake(game_df)[1],
                                'red_nashor_herald' : get_nashor_herald(game_df)[1],
                                
                                'sentence' : get_sentence(game_df),
                                'killer' : get_kill(game_df)[0],
                                'victim' : get_kill(game_df)[1],
                                'tower' : get_tower(game_df),
                                
                                'blue_set_score' : get_set_score(game_df,'blue'),
                                'red_set_score' : get_set_score(game_df,'red')}).set_index('timestamp')
                                
                                
                                
    return processed_df
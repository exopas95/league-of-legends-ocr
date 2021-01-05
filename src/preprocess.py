import numpy as np
import pandas as pd
import time
import re
import math
import src.constants as constants
import operator


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
    game_df = df.loc[timestamps[0]:timestamps[-1]]                                     # Get remain of the start to the end of a game
    return game_df.dropna(subset=['timestamp'])                                    # remove replay

""" Figure out language of the game
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def is_korean(df):
    game_df = get_game_df(df)
    is_korean = True
    for x in game_df.index:
        if 'minions' in ' '.join(game_df.notice.loc[x]).lower() or 'dragon' in ' '.join(game_df.notice.loc[x]).lower() or 'tower' in ' '.join(game_df.notice.loc[x]).lower():
            is_korean = False
            break
    return is_korean

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

def df_target(df, keywords):
    target_index = []
    for keyword in keywords:
        for x in df.index:
            try:
                if keyword in ' '.join(df.notice.loc[x]).lower():
                    target_index.append(x)
            except:
                pass
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
    df_drake_pre = df_target(df, ['드래곤','dragon'])
    df_drake = deduplicate(df_drake_pre)
    blue = []
    red = []
    blue_dra_stack = 0
    red_dra_stack = 0
    has_error = ''
    total_stack = blue_dra_stack + red_dra_stack
    
    if len(seq) > 0:
        for x in df.index :
            if x in df_drake.index:
                if '드래곤' in df.notice.loc[x] or 'dragon' in ' '.join(df.notice.loc[x]).lower() :
                    if '파랑' in df.notice.loc[x] or 'blue' in ' '.join(df.notice.loc[x]).lower() :
                        blue_dra_stack += 1
                        red.append(np.nan)
                        total_stack = blue_dra_stack + red_dra_stack
                        if total_stack < 3:
                            blue.append(has_error+seq[total_stack-1]+'DRAKE')
                        elif total_stack >= 3:
                            if (blue_dra_stack > 4) or (red_dra_stack >= 4):      #red got 4 dragon or blue already got 4 dragon 
                                blue.append(has_error+'ELDER'+'DRAKE')
                            else:
                                blue.append(has_error+seq[2]+'DRAKE')
                    elif '빨강' in df.notice.loc[x] or 'red' in ' '.join(df.notice.loc[x]).lower() :
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
    else: 
        for x in df.index :
            if x in df_drake.index:
                if '드래곤' in df.notice.loc[x] or 'dragon' in ' '.join(df.notice.loc[x]).lower() :
                    if '파랑' in df.notice.loc[x] or 'blue' in ' '.join(df.notice.loc[x]).lower() :
                        blue_dra_stack += 1
                        red.append(np.nan)
                        total_stack = blue_dra_stack + red_dra_stack
                        if total_stack < 3:
                            blue.append('DRAKE')
                        elif total_stack >= 3:
                            if (blue_dra_stack > 4) or (red_dra_stack >= 4):      #red got 4 dragon or blue already got 4 dragon 
                                blue.append(has_error+'ELDER'+'DRAKE')
                            else:
                                blue.append(has_error+'DRAKE')
                    elif '빨강' in df.notice.loc[x] or 'red' in ' '.join(df.notice.loc[x]).lower() :
                        red_dra_stack += 1
                        blue.append(np.nan)
                        total_stack = blue_dra_stack + red_dra_stack
                        if total_stack < 3:
                            red.append('DRAKE')
                        elif total_stack >= 3:
                            if (red_dra_stack > 4) or (blue_dra_stack >= 4):
                                red.append(has_error+'ELDER'+' DRAKE')
                            else:
                                red.append(has_error+'DRAKE')
                    else:                                         #slain drake but don't know team
                        red.append('UNKNOWN'+' DRAKE')
                        blue.append('UNKNOWN'+' DRAKE')
                        has_error = '[ERROR]'
                else:
                    red.append(np.nan)
                    blue.append(np.nan)
            else:
                red.append(np.nan)
                blue.append(np.nan)   
    return blue,red

""" Get tuple of list of nashor/herald(blue, red) from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_nashor_herald(df) :
    blue = []
    red = []
    df_nashor_pre = df_target(df, ['내셔','nashor'])
    df_herald_pre = df_target(df, ['전령','herald'])
    df_nashor = deduplicate(df_nashor_pre)
    df_herald = deduplicate(df_herald_pre)
    df_object = pd.concat([df_nashor, df_herald])
    for x in df.index :
        if x in df_object.index :
            if '파랑' in df.notice.loc[x] or 'blue' in ' '.join(df.notice.loc[x]).lower() :
                if '남작' in df.notice.loc[x] or 'nashor' in ' '.join(df.notice.loc[x]).lower() :
                    red.append(np.nan)
                    blue.append('nashor')
                elif '전령' in df.notice.loc[x] or 'herald' in ' '.join(df.notice.loc[x]).lower() :
                    red.append(np.nan)
                    blue.append('summon_herald')
                else:
                    red.append(np.nan)
                    blue.append(np.nan)
            elif '빨강' in df.notice.loc[x] or 'red' in ' '.join(df.notice.loc[x]).lower() :
                if '남작' in df.notice.loc[x] or 'nashor' in ' '.join(df.notice.loc[x]).lower() :
                    blue.append(np.nan)
                    red.append('nashor')
                elif '전령' in df.notice.loc[x] or 'herald' in ' '.join(df.notice.loc[x]).lower() :
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

""" Get Dictionary of User's ID from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_user_dic(df) :
    str_set = constants.cols[0:10]          # str_set = ['blue_top_port', ... 'red_sup_port']
    user_dic = {}                           # return dictionary
    team_dic = {}                           # team dictionary
    for line, i in zip(str_set,range(10)) :
        BOW_0, BOW_1 = {}, {}                            # Bag of Words
        for j in range(len(df)) :
            try :
                if df.iloc[j,i][1] in BOW_0 :
                    BOW_0[ df.iloc[j,i][1] ] += 1
                else :
                    BOW_0[ df.iloc[j,i][1] ] = 1
            except :
                continue
            try :
                if df.iloc[j,i][0] in BOW_1 :
                    BOW_1[ df.iloc[j,i][0] ] += 1
                else :
                    BOW_1[ df.iloc[j,i][0] ] = 1
            except :
                continue
        likely_0, likely_1 = max(BOW_0.items(), key=operator.itemgetter(1))[0], max(BOW_1.items(), key=operator.itemgetter(1))[0]
        try :
            if likely_0 in team_dic :
                team_dic[ likely_0 ] += 1
            else :
                team_dic[ likely_0 ] = 1
        except :
            continue
        try :
            if likely_1 in team_dic :
                team_dic[ likely_1 ] += 1
            else :
                team_dic[ likely_1 ] = 1
        except :
            continue
        if i == 4 :
            blue_team = max(team_dic.items(), key=operator.itemgetter(1))[0]
            team_dic = {}
        elif i == 9 :
            red_team = max(team_dic.items(), key=operator.itemgetter(1))[0]
        user_dic[ line[:-5]] = [max(BOW_0.items(), key=operator.itemgetter(1))[0], max(BOW_0.values()),
                                max(BOW_1.items(), key=operator.itemgetter(1))[0], max(BOW_1.values())]
    for line in str_set :
        line = line[:-5]
        if user_dic[ line ][1] > 800 :           # minimum count of id appearance in port
            if user_dic[ line ][0] != blue_team and user_dic[ line ][0] != red_team :
                user_dic[ line ] = user_dic[ line ][0]
        elif user_dic[ line ][3] > 800 :
            if user_dic[ line ][2] != blue_team and user_dic[ line ][0] != red_team :
                user_dic[ line ] = user_dic[ line ][2]
    return user_dic

""" rough similarity calcaulator for user_id just compare all characters of x and y iterately
    - param x, y : str which to calculate
    - type x, y : str
"""
def calculator_similar_id(x,y) :
    cnt = 0
    try :
        for x_char, y_char in zip(x,y) :
            if x_char == y_char :
                cnt += 1
    except :
        cnt = 0
    return cnt/len(y)

def calculator_similar(x,y) :
    if flag_is_korean:
        cnt = 0
        try :
            for x_char in x:
                for y_char in y :
                    if x_char == y_char :
                        cnt += 1
        except :
            cnt = 0
        return cnt/len(y)   
    else:
        cnt = 0
        try :
            for x_char in x.split(' '):
                if x_char.lower() in ['dragon','nashor','herald']:
                    return 0
                for y_char in y.split(' ') :
                    y_char = re.sub('[^a-zA-Z가-힣0-9- ]+', '', y_char)
                    if x_char.lower() == y_char.lower() :
                        cnt += 1
            return cnt/len(y.split(' '))
        except :
            return 0

def get_sentence(df) :


""" Get DataFrame of classified notice from input dataframe
    - param df: Input dataframe (Outcome from Vision) which will be preprocessed 
    - type df: dataframe
"""
def get_sentence(df) :
    # make list to str such as
    # ['AF', 'Mystic', '님', '이', '서', 'T', 'SOHwan', '님', '을', '처치', '했습니다', '!']
    # to 'AFMystic님이서TSOHwan님을처치했습니다'
    def list_to_str(x) :
        if flag_is_korean:
            result = ''.join(x)
            result = re.sub('[^a-zA-Z가-힣0-9]+', '', result) # alphabet, number, korean is all things we are interested in
            if result :
                return result
            else :
                result = np.nan
            return result
        else:    
            result = ' '.join(x)
            result = re.sub('[^a-zA-Z가-힣0-9- ]+', '', result)
            if result :
                return result
            else :
                result = np.nan
            return result

    def notice_cleaner(df) :
        text = df.notice.apply(
            lambda x : list_to_str(x)
        )
        return text            

    # judge the notice x is what about
    # 0.65 is asymptotical value.
    # usually when max similarity <= 0.5~ 0.6 it is just nuisance
    # when max similarity >= 0.7 , it is worthwhile to consider
    def judge_sentence(x) :
        if flag_is_korean:
            if max(x) <= 0.65 :
                return np.nan
            return x.astype(float).idxmax()
        else:            
            if max(x) <= 0.9 :
                return np.nan
            return x.astype(float).idxmax()

    if flag_is_korean:
        similar = pd.DataFrame(columns=['text']+constants.text_str) # similarity matrix
        similar['text'] = notice_cleaner(df)
    
        for i in constants.text_str :
            similar[i] = similar.text.apply(
                lambda x : calculator_similar(x, constants.total_sentence[i])
            )
        
    else:   
        similar = pd.DataFrame(columns=['text']+constants.eng_text_str)
        similar['text'] = notice_cleaner(df)
        
        for i in constants.eng_text_str :
            similar[i] = similar.text.apply(
                lambda x : calculator_similar(x, constants.eng_total_sentencetotal_sentence[i])
            )

    real_text = []
    for i in range(len(similar)) :
        real_text.append(judge_sentence((similar.iloc[i,:][1:])))

    similar['real_text'] = real_text  # this is what we want 
    
    
    sentence = similar.real_text.copy().fillna("0")

    tmp = sentence.iloc[0]
    tmp_idx = int(0)
    for i in range(1,len(sentence)) :
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

def get_kill(df, user_dic) :
    df_use = df.copy()
    df_use['sentence'] = get_sentence(df_use)
    
    def killer_victim_find(x):
        if flag_is_korean:
            killer_id, victim_id = np.nan, np.nan
            cnt, nim_cnt = 0, 0
            tmp = x.copy()
            for text in tmp :
                if text == '님' :
                    nim_cnt += 1
                max_val, max_str = 0, np.nan
                for line in user_dic:
                    user_id = user_dic.get(line)
                    if ( calculator_similar_id(text, user_id) > max_val )  and ( calculator_similar_id(text, user_id) >= 0.75 ) :
                        max_val = calculator_similar_id(text, user_id)
                        max_str = user_id
                if max_val >= 0.75 :
                    tmp[ tmp.index(text) ] = max_str
                for line in user_dic :
                    user_id = user_dic.get(line)
                    if (calculator_similar_id(text, user_id) == max_val) and (max_val >= 0.75)  :
                        try :
                            if( type(user_id) == int or type(user_id) == str) and (cnt == 0) :
                                killer_id = user_id 
                                cnt += 1
                            elif( type(user_id) == int or type(user_id) == str) and (cnt == 1) :
                                victim_id = user_id
                                cnt += 1
                            elif(type(user_id) == int or type(user_id) == str) and (cnt >= 2) :
                                cnt += 1    
                        except :
                            continue
            if cnt == 2 :
                return killer_id, victim_id
            elif nim_cnt == 2 :
                try :
                    loc = []
                    cnt, check = 0, 0
                    for i in tmp :
                        if i == '님' :
                            loc.append(cnt-1)
                            check += 1
                        cnt += 1
                    if check == 2 :
                        killer_id = tmp[loc[0]]
                        victim_id = tmp[loc[1]]
                        return killer_id, victim_id
                except :
                    return np.nan, np.nan
            else :
                return np.nan, np.nan
        else:    
            killer_id, victim_id = np.nan, np.nan
            cnt = 0
            for text in x :
                for line in user_dic:
                    user_id = user_dic.get(line)
                    if calculator_similar_id(text, user_id) >= 0.75 :
                        try :
                            if( type(user_id) == int or type(user_id) == str) and (cnt == 0) :
                                killer_id = user_id 
                                cnt += 1
                            elif( type(user_id) == int or type(user_id) == str) and (cnt == 1) :
                                victim_id = user_id
                                cnt += 1
                        except :
                            continue
            if cnt == 2 :
                return killer_id, victim_id
            else :
                return np.nan, np.nan

    killer, victim = [], []
    for x in range(len(df_use.index)) :
        if 'blood' in df_use.sentence[x] :
            killer.append( np.nan )
            victim.append( np.nan )
        elif 'kill' in df_use.sentence[x] :
            try :
                ki_0, vi_0 = killer_victim_find(df_use.notice[x])
            except :
                ki_0, vi_0 = np.nan, np.nan
            try :
                ki_1, vi_1 = killer_victim_find(df_use.notice[x+1])
            except :
                ki_1, vi_1 = np.nan, np.nan
            try :
                ki_2, vi_2 = killer_victim_find(df_use.notice[x+2])
            except :
                ki_2, vi_2 = np.nan, np.nan
                
            try :
                if ( type(ki_0) == int or type(ki_0) == str)  :
                    killer.append(ki_0)
                elif ( type(ki_1) == int or type(ki_1) == str) :
                    killer.append(ki_1)
                elif ( type(ki_2) == int or type(ki_2) == str) :
                    killer.append(ki_2)
                else :
                    killer.append( np.nan )
            except :
                killer.append( np.nan )
            try :
                if ( type(vi_0) == int or type(vi_0) == str)  :
                    victim.append(vi_0)
                elif ( type(vi_1) == int or type(vi_1) == str) :
                    victim.append(vi_1)
                elif ( type(vi_2) == int or type(vi_2) == str) :
                    victim.append(vi_2)
                else :
                    victim.append( np.nan )
            except :
                victim.append( np.nan )
        else :
            killer.append(np.nan)
            victim.append(np.nan)
    return killer, victim
    

##########예전 killer, victim       
    # killer, victim = [], []
    # for x in range(len(df_use.index)) :
    #     if 'blood' in df_use.sentence[x] :
    #         killer.append( np.nan )
    #         victim.append( np.nan )
    #     elif 'kill' in df_use.sentence[x] :
    #         ki_0, vi_0 = killer_victim_find(df_use.notice[x])
    #         try :
    #             ki_1, vi_1 = killer_victim_find(df_use.notice[x+1])
    #         except :
    #             ki_1, vi_1 = np.nan, np.nan
    #         try :
    #             ki_2, vi_2 = killer_victim_find(df_use.notice[x+2])
    #         except :
    #             ki_2, vi_2 = np.nan, np.nan
                
    #         try :
    #             if ( type(ki_0) == int or type(ki_0) == str)  :
    #                 killer.append(ki_0)
    #             elif ( type(ki_1) == int or type(ki_1) == str) :
    #                 killer.append(ki_1)
    #             elif ( type(ki_2) == int or type(ki_2) == str) :
    #                 killer.append(ki_2)
    #             else :
    #                 killer.append( np.nan )
    #         except :
    #             killer.append( np.nan )
    #         try :
    #             if ( type(vi_0) == int or type(vi_0) == str)  :
    #                 victim.append(vi_0)
    #             elif ( type(vi_1) == int or type(vi_1) == str) :
    #                 victim.append(vi_1)
    #             elif ( type(vi_2) == int or type(vi_2) == str) :
    #                 victim.append(vi_2)
    #             else :
    #                 victim.append( np.nan )
    #         except :
    #             victim.append( np.nan )
    #     else :
    #         killer.append(np.nan)
    #         victim.append(np.nan)
    # return killer, victim

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
def result_process(df, is_korean) :
    game_df = get_game_df(df)
    global flag_is_korean
    flag_is_korean = is_korean
    user_dic = get_user_dic(df)
    processed_df = pd.DataFrame({"video_timestamp": get_video_timestamp(game_df),
                                'timestamp' : get_timestamp(game_df),
                                '200_teamgold' : get_teamgold(game_df, 'red'),

                                '206_level' : get_level(game_df, 'red', 'top'),
                                '207_level' : get_level(game_df, 'red', 'jug'),
                                '208_level' : get_level(game_df, 'red', 'mid'),
                                '209_level' : get_level(game_df, 'red', 'bot'),
                                '210_level' : get_level(game_df, 'red', 'sup'),

                                '206_cs' : get_cs(game_df, 'red', 'top'),
                                '206_shutdown' : get_shutdown(game_df, 'red', 'top'),
                                '206_k' : get_kda(game_df, 'red', 'top', 'k'),
                                '206_d' : get_kda(game_df, 'red', 'top', 'd'),
                                '206_a' : get_kda(game_df, 'red', 'top', 'a'),

                                '207_cs' : get_cs(game_df, 'red', 'jug'),
                                '207_shutdown' : get_shutdown(game_df, 'red', 'jug'),
                                '207_k' : get_kda(game_df, 'red', 'jug', 'k'),
                                '207_d' : get_kda(game_df, 'red', 'jug', 'd'),
                                '207_a' : get_kda(game_df, 'red', 'jug', 'a'),

                                '208_cs' : get_cs(game_df, 'red', 'mid'),
                                '208_shutdown' : get_shutdown(game_df, 'red', 'mid'),
                                '208_k' : get_kda(game_df, 'red', 'mid', 'k'),
                                '208_d' : get_kda(game_df, 'red', 'mid', 'd'),
                                '208_a' : get_kda(game_df, 'red', 'mid', 'a'),

                                '209_cs' : get_cs(game_df, 'red', 'bot'),
                                '209_shutdown' : get_shutdown(game_df, 'red', 'bot'),
                                '209_k' : get_kda(game_df, 'red', 'bot', 'k'),
                                '209_d' : get_kda(game_df, 'red', 'bot', 'd'),
                                '209_a' : get_kda(game_df, 'red', 'bot', 'a'),

                                '210_cs' : get_cs(game_df, 'red', 'sup'),
                                '210_shutdown' : get_shutdown(game_df, 'red', 'sup'),
                                '210_k' : get_kda(game_df, 'red', 'sup', 'k'),
                                '210_d' : get_kda(game_df, 'red', 'sup', 'd'),
                                '210_a' : get_kda(game_df, 'red', 'sup', 'a'),

                                '100_teamgold' : get_teamgold(game_df, 'blue'),
                                '101_level' : get_level(game_df, 'blue', 'top'),
                                '102_level' : get_level(game_df, 'blue', 'jug'),
                                '103_level' : get_level(game_df, 'blue', 'mid'),
                                '104_level' : get_level(game_df, 'blue', 'bot'),
                                '105_level' : get_level(game_df, 'blue', 'sup'),

                                '101_cs' : get_cs(game_df, 'blue', 'top'),
                                '101_shutdown' : get_shutdown(game_df, 'blue', 'top'),
                                '101_k' : get_kda(game_df, 'blue', 'top', 'k'),
                                '101_d' : get_kda(game_df, 'blue', 'top', 'd'),
                                '101_a' : get_kda(game_df, 'blue', 'top', 'a'),

                                '102_cs' : get_cs(game_df, 'blue', 'jug'),
                                '102_shutdown' : get_shutdown(game_df, 'blue', 'jug'),
                                '102_k' : get_kda(game_df, 'blue', 'jug', 'k'),
                                '102_d' : get_kda(game_df, 'blue', 'jug', 'd'),
                                '102_a' : get_kda(game_df, 'blue', 'jug', 'a'),

                                '103_cs' : get_cs(game_df, 'blue', 'mid'),
                                '103_shutdown' : get_shutdown(game_df, 'blue', 'mid'),
                                '103_k' : get_kda(game_df, 'blue', 'mid', 'k'),
                                '103_d' : get_kda(game_df, 'blue', 'mid', 'd'),
                                '103_a' : get_kda(game_df, 'blue', 'mid', 'a'),

                                '104_cs' : get_cs(game_df, 'blue', 'bot'),
                                '104_shutdown' : get_shutdown(game_df, 'blue', 'bot'),
                                '104_k' : get_kda(game_df, 'blue', 'bot', 'k'),
                                '104_d' : get_kda(game_df, 'blue', 'bot', 'd'),
                                '104_a' : get_kda(game_df, 'blue', 'bot', 'a'),

                                '105_cs' : get_cs(game_df, 'blue', 'sup'),
                                '105_shutdown' : get_shutdown(game_df, 'blue', 'sup'),
                                '105_k' : get_kda(game_df, 'blue', 'sup', 'k'),
                                '105_d' : get_kda(game_df, 'blue', 'sup', 'd'),
                                '105_a' : get_kda(game_df, 'blue', 'sup', 'a'),
                                
                                '101_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','top')),
                                '102_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','jug')),
                                '103_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','mid')),
                                '104_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','bot')),
                                '105_vision_score' : valid_vision_score(get_vision_score(game_df,'blue','sup')),
                                
                                '206_vision_score' : valid_vision_score(get_vision_score(game_df,'red','top')),
                                '207_vision_score' : valid_vision_score(get_vision_score(game_df,'red','jug')),
                                '208_vision_score' : valid_vision_score(get_vision_score(game_df,'red','mid')),
                                '209_vision_score' : valid_vision_score(get_vision_score(game_df,'red','bot')),
                                '210_vision_score' : valid_vision_score(get_vision_score(game_df,'red','sup')),
                                
                                '100_tower_score' : get_tower_score(game_df,'blue'),
                                '200_tower_score' : get_tower_score(game_df, 'red'),

                                '100_drake' : get_drake(game_df)[0],
                                '100_nashor_herald' : get_nashor_herald(game_df)[0],
                                '200_drake' : get_drake(game_df)[1],
                                '200_nashor_herald' : get_nashor_herald(game_df)[1],
                                
                                'sentence' : get_sentence(game_df),
                                'killer' : get_kill(game_df,user_dic)[0],
                                'victim' : get_kill(game_df,user_dic)[1],
                                'tower' : get_tower(game_df),
                               
                                '100_set_score' : get_set_score(game_df,'blue'),
                                '200_set_score' : get_set_score(game_df,'red')}).set_index('timestamp')
                                
                                                            
    return processed_df
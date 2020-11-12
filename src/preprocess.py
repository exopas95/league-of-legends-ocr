import numpy as np
import pandas as pd
import re

def judge_kda(x) :
    try :
        if np.isnan(x) :
            return x
    except :
        word = re.sub(r'[^0-9/]', '', x)

        n_slash = 0
        n_seven = 0
        seven_index = []
        for i, char in enumerate(word) :
            if (char == '/') :
                n_slash += 1
            elif (char == '7') :
                n_seven += 1
                seven_index.append(i)

        if n_slash == 2 :
            kda = re.split('/', word)

        else :
            if (n_seven == 1) & (n_slash == 1) :
                kda = re.split('/|7', word)

            else :
                rep = (('77', 'a/'), ('7/', 'a/'), ('777', '/a/'), ('7777', 'a/a/'))
                for r in reversed(rep) :
                    word = word.replace(*r)
                kda = re.split('/|7', word)
                kda = list(filter(lambda x: x != '', kda))
                if len(word)-1 in seven_index :
                    kda[-1] += '7'

        kda = [re.sub('a', '7', x) for x in kda]

        if len(kda) == 3 :
            try :
                kda = [int(x) for x in kda]
                return kda
            except :
                return np.nan
        else :
            return np.nan


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
            if (a[i] >= temp) & (a[i]<1000) :
                a_inc.append(a[i])
                temp = a[i]
                i += 1
            else :
                if coin > ths :
                    i -= ths
                    coin = 0
                    temp = a[i-1]
                    a_inc = a_inc[:-(ths+2)]
                    a_inc.append(np.nan)
                    a_inc.append(a[i-1])
                else :
                    a_inc.append(np.nan)
                    i += 1
                    coin += 1
    return a_inc


def make_dec(a, ths) :
    a_temp = []
    i = len(a)-1
    temp = 0
    coin = 0
    while i >= 0 :
        if np.isnan(a[i]) :
            a_temp.append(np.nan)
            i -= 1
        else :
            if (a[i] <= temp) & (a[i]<1000) :
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
    
    a_dec = [x for x in reversed(a_temp)]
    return a_dec


def make_monotonic(a, ths) :
    a_mono = []
    for i, (x,y) in enumerate(zip(make_dec(a, ths), make_inc(a, ths))) :
        if x == y :
            a_mono.append(x)
        else :
            a_mono.append(np.nan)
    return a_mono


def get_game_df(df) :
    df['timestamp'] = df['timestamp'].apply(lambda x: np.nan if len(x)==0 else x)
    timestamps = df.dropna(subset=['timestamp']).index
    return df.loc[timestamps[0]:timestamps[-1]]


def get_timestamp(df) : 
    l = []
    for x in df.timestamp.values :
        try :
            if bool(re.match(r'[\d\d]+:[\d\d]+', x[0])) :
                l.append(x[0])
            else :
                l.append(np.nan)
        except :
            l.append(x)
    return l

def get_teamgold(df, side) :
    l = []
    def isgold(l, side) :
        s = np.nan
        if side =='blue' :
            l = reversed(l)
        elif side == 'red' :
            l = l            
        for x in l :
            if len(x) > 3 :
                s = x
                break
            else :
                continue
        return s

    for x in df[side+'_teamgold'].values :
        try :
            raw_gold = isgold(x, side)
            gold = float(re.sub(',', '.', re.sub(r'[^0-9.,]', '', raw_gold)))
            l.append(gold)            
        except :
            l.append(np.nan)
    return make_monotonic(l, 5)


def get_cs(df, side, pos) :
    l = []
    for x in df[side+'_'+pos+'_cs'].values :
        if len(x) > 0 :
            try :
                l.append(float(x[0]))
            except :
                l.append(np.nan)
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)

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
                l.append(judgekda(x[0])[kda_index])
            except :
                l.append(np.nan)
        else :
            l.append(np.nan)
    return make_monotonic(l, 5)


def get_notice(df) :
    blue = []
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
                elif ('포탑' in x) :
                    if '번째' in x :
                        blue.append('turret')
                        red.append(np.nan)
                    else :
                        red.append('turret')
                        blue.append(np.nan)
                else :
                    red.append(np.nan)
                    blue.append('unknown')
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
    return blue, red

def result_process(df) :
    game_df = get_game_df(df)
    processed_df = pd.DataFrame({'timestamp' : get_timestamp(game_df),
                                'red_top_port' : game_df.red_top_port.values
                                'blue_top_port' : game_df.blue_top_port.values

                                'red_teamgold' : get_teamgold(game_df, 'red'),
                                'red_top_cs' : get_cs(game_df, 'red', 'top'),
                                'red_top_k' : get_kda(game_df, 'red', 'top', 'k'),
                                'red_top_d' : get_kda(game_df, 'red', 'top', 'd'),
                                'red_top_a' : get_kda(game_df, 'red', 'top', 'a'),

                                'red_jug_cs' : get_cs(game_df, 'red', 'jug'),
                                'red_jug_k' : get_kda(game_df, 'red', 'jug', 'k'),
                                'red_jug_d' : get_kda(game_df, 'red', 'jug', 'd'),
                                'red_jug_a' : get_kda(game_df, 'red', 'jug', 'a'),

                                'red_mid_cs' : get_cs(game_df, 'red', 'mid'),
                                'red_mid_k' : get_kda(game_df, 'red', 'mid', 'k'),
                                'red_mid_d' : get_kda(game_df, 'red', 'mid', 'd'),
                                'red_mid_a' : get_kda(game_df, 'red', 'mid', 'a'),

                                'red_bot_cs' : get_cs(game_df, 'red', 'bot'),
                                'red_bot_k' : get_kda(game_df, 'red', 'bot', 'k'),
                                'red_bot_d' : get_kda(game_df, 'red', 'bot', 'd'),
                                'red_bot_a' : get_kda(game_df, 'red', 'bot', 'a'),

                                'red_sup_cs' : get_cs(game_df, 'red', 'sup'),
                                'red_sup_k' : get_kda(game_df, 'red', 'sup', 'k'),
                                'red_sup_d' : get_kda(game_df, 'red', 'sup', 'd'),
                                'red_sup_a' : get_kda(game_df, 'red', 'sup', 'a'),

                                'red_notice' : get_notice(game_df)[0],

                                'blue_teamgold' : get_teamgold(game_df, 'blue'),

                                'blue_top_cs' : get_cs(game_df, 'blue', 'top'),
                                'blue_top_k' : get_kda(game_df, 'blue', 'top', 'k'),
                                'blue_top_d' : get_kda(game_df, 'blue', 'top', 'd'),
                                'blue_top_a' : get_kda(game_df, 'blue', 'top', 'a'),

                                'blue_jug_cs' : get_cs(game_df, 'blue', 'jug'),
                                'blue_jug_k' : get_kda(game_df, 'blue', 'jug', 'k'),
                                'blue_jug_d' : get_kda(game_df, 'blue', 'jug', 'd'),
                                'blue_jug_a' : get_kda(game_df, 'blue', 'jug', 'a'),

                                'blue_mid_cs' : get_cs(game_df, 'blue', 'mid'),
                                'blue_mid_k' : get_kda(game_df, 'blue', 'mid', 'k'),
                                'blue_mid_d' : get_kda(game_df, 'blue', 'mid', 'd'),
                                'blue_mid_a' : get_kda(game_df, 'blue', 'mid', 'a'),

                                'blue_bot_cs' : get_cs(game_df, 'blue', 'bot'),
                                'blue_bot_k' : get_kda(game_df, 'blue', 'bot', 'k'),
                                'blue_bot_d' : get_kda(game_df, 'blue', 'bot', 'd'),
                                'blue_bot_a' : get_kda(game_df, 'blue', 'bot', 'a'),

                                'blue_sup_cs' : get_cs(game_df, 'blue', 'sup'),
                                'blue_sup_k' : get_kda(game_df, 'blue', 'sup', 'k'),
                                'blue_sup_d' : get_kda(game_df, 'blue', 'sup', 'd'),
                                'blue_sup_a' : get_kda(game_df, 'blue', 'sup', 'a'),

                                'blue_notice' : get_notice(game_df)[1]}).set_index('timestamp')
    return processed_df
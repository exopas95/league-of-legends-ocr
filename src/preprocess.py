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
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


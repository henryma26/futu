# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:07:32 2023

@author: user
"""

import os
import pandas as pd

with open('hkstocksfutu_20230224.txt', 'r') as f:
    stocklist = f.read().splitlines()


###find out the hk stocks that have enough data for me to analyze, mainly between 2020-2023
def findstock():
    stocksmorethan900 = []
    for stock in stocklist:
        
        if os.path.exists(f'{stock}.pkl'):
            df = pd.read_pickle(f'{stock}.pkl')
            if len(df) >= 900:
                stocksmorethan900.append(stock)
            
    return stocksmorethan900

data = findstock()
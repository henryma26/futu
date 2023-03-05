# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:07:32 2023

@author: user
"""

import os
import pandas as pd

with open('hkstocksfutu_20230224.txt', 'r') as f:
    stocklist = f.read().splitlines()

# data = pd.read_pickle('stocksmorethan900.pkl')

###find out the hk stocks that have enough data for me to analyze, mainly between 2020-2023
def findstock():
    stocksmorethan900 = []
    for stock in stocklist:
        
        if os.path.exists(f'{stock}.pkl'):
            df = pd.read_pickle(f'{stock}.pkl')
            if len(df) >= 900:
                stocksmorethan900.append(stock)
            
    return stocksmorethan900

###find out the hk stocks that were above 250sma or below 250sma
def findstocksma(stocks):
    above250sma = []
    below250sma = []
    
    for stock in stocks:
        df_stock = pd.read_pickle(f'{stock}.pkl')
        df_stock['250sma'] = df_stock['close'].rolling(window=250).mean()
        
        start_date = '2021-02-17 00:00:00'
        if start_date in df_stock['time_key'].values:
            start_close = df_stock.loc[df_stock['time_key'] == start_date, 'close'].values[0]
            start_sma250 = df_stock.loc[df_stock['time_key'] == start_date, '250sma'].values[0]
            if start_close > start_sma250:
                above250sma.append(stock)
            else:
                below250sma.append(stock)
        # print(start_close)

    return df_stock, above250sma, below250sma

data = findstock()

bb = findstocksma(data)

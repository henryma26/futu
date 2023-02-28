# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:51:58 2023

@author: henryma
"""

import pandas as pd

df = pd.read_pickle('stocksmorethan900.pkl')

stocklist = df[0].tolist()
stocklist.append('hsi')

dailychange = []
datetocheck = '2021-02-17 00:00:00'
for stock in stocklist:
    df = pd.read_pickle(f'{stock}.pkl')
    # print(df)
    

    # calculate the percentage change, shifted by 1 row
    df['price_change_pct'] = df['close'].pct_change(periods=1) * 100

    # display the DataFrame
    if datetocheck in df['time_key'].values:
    
        close_value = df.loc[df['time_key'] == datetocheck, 'price_change_pct'].values[0]
        print(close_value)
        
        tempdict = {'stock': stock, 'price_change': round(close_value,3)}
        dailychange.append(tempdict)
    
    else:
        print(f"{stock} doesn't have data of this date")
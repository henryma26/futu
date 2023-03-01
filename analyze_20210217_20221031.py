# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:51:58 2023

@author: henryma
"""

import pandas as pd
import time
start_time = time.time()

df = pd.read_pickle('stocksmorethan900.pkl')

stocklist = df[0].tolist()
stocklist.append('hsi')

pctin2years = []
start_date = '2021-02-17 00:00:00'
end_date = '2022-10-31 00:00:00'
for stock in stocklist:
    df2 = pd.read_pickle(f'{stock}.pkl')
    # print(df)
    
    # display the DataFrame
    if start_date in df2['time_key'].values and end_date in df2['time_key'].values:
        print("yes")
        # start_date = '2021-02-17 00:00:00'
        # end_date = '2022-10-31 00:00:00'
        
        start_close = df2.loc[df2['time_key'] == start_date, 'close'].values[0]
        end_close = df2.loc[df2['time_key'] == end_date, 'close'].values[0]
        
        price_change_pct = (end_close / start_close - 1) * 100
        
        tempdict = {'stock': stock, 'price_change': round(price_change_pct,3)}
        pctin2years.append(tempdict)
    
    else:
        print(f"{stock} doesn't have data of this date")
        
        




end_time = time.time()

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

# df2 = pd.read_pickle('HK.00001.pkl')
# start_date = '2019-02-04 00:00:00'
# end_date = '2019-02-12 00:00:00'

# start_close = df2.loc[df2['time_key'] == start_date, 'close'].values[0]
# end_close = df2.loc[df2['time_key'] == end_date, 'close'].values[0]

# price_change_pct = (end_close / start_close - 1) * 100
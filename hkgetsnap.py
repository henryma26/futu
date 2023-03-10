# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:42:19 2023

This file is used to capture the snapshot of the market realtime
"""

import pandas as pd
from futu import *
import time

def checkstatus():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    
    ret, data= quote_ctx.get_plate_stock('HK.Motherboard')
    stock_list = data['code'].tolist()
    quote_ctx.close()
    
    with open('to_remove.txt', 'r') as f:
        to_remove = f.read().splitlines()
        
    for stock in to_remove:
        stock_list.remove(stock)
    
    return stock_list
\
    
def get_snapshot(remain_hkstocks):
    stocks_data = []
    count = 0
    stockrange = 0
    howmanytimes = round(len(remain_hkstocks)/400)
    
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    while count < howmanytimes:
        ret, data = quote_ctx.get_market_snapshot(remain_hkstocks[stockrange:stockrange+400])
        
        stocks_data.append(data)
        stockrange+=400
        count+=1
        
    return stocks_data

remain_hkstocks = checkstatus()
snapshot = get_snapshot(remain_hkstocks)
final = pd.concat(snapshot)
top_10_trate = final.nlargest(10, 'turnover_rate')
top_10_am = final.nlargest(10, 'amplitude')
                        
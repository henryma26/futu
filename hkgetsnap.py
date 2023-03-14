# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:16:14 2023

@author: henryma
"""

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
    
    quote_ctx.close()
    
    return stocks_data

def myfilter(final):
    my_filter = []
    for index, row in final.iterrows():
        if row['last_price'] > row['prev_close_price'] and row['turnover'] > 200000 and row['close_price_5min'] != 0:
            my_filter.append(row['code'])
    
    return my_filter
    
def comparesma250(getstock):
    # getstock = getstock[300:]
    countstock = len(getstock)
    numberofreset = round(len(getstock)/100)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    
    for stock in getstock[0:100]:
        ret_sub, err_message = quote_ctx.subscribe(stock, [SubType.K_DAY], subscribe_push=False)
        # 先订阅 K 线类型。订阅成功后 FutuOpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = quote_ctx.get_cur_kline(stock, 2, KLType.K_DAY, AuType.QFQ)  # 获取港股00700最近2个 K 线数据
            if ret == RET_OK:
                print(data)
                # print(data['turnover_rate'][0])   # 取第一条的换手率
                # print(data['turnover_rate'].values.tolist())   # 转为 list
            else:
                print('error:', data)
        else:
            print('subscription failed', err_message)
    quote_ctx.close()
    
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    for stock in getstock[100:200]:
        ret_sub, err_message = quote_ctx.subscribe(stock, [SubType.K_DAY], subscribe_push=False)
        # 先订阅 K 线类型。订阅成功后 FutuOpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = quote_ctx.get_cur_kline(stock, 2, KLType.K_DAY, AuType.QFQ)  # 获取港股00700最近2个 K 线数据
            if ret == RET_OK:
                print(data)
                # print(data['turnover_rate'][0])   # 取第一条的换手率
                # print(data['turnover_rate'].values.tolist())   # 转为 list
            else:
                print('error:', data)
        else:
            print('subscription failed', err_message)
    quote_ctx.close()
        
    return numberofreset
    
remain_hkstocks = checkstatus()
snapshot = get_snapshot(remain_hkstocks)
final = pd.concat(snapshot)
getstock = myfilter(final)
getstock2 = comparesma250(getstock)
top_10_trate = final.nlargest(10, 'turnover_rate')
top_10_am = final.nlargest(10, 'amplitude')

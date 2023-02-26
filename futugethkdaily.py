# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:22:27 2022

@author: henryma
"""

from futu import *
import time
import pandas as pd
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

with open('hkstocksfutu_20230224.txt', 'r') as f:
    stocklist = f.read().splitlines()

#stocklist = stocklist[1600:1700]
count = 0
timetoloop = round(len(stocklist)/100)
stockrange = 0
stockloop = 0

while count < timetoloop:
    
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    stocktoget = stocklist[stockrange:stockrange+100]
    
    while stockloop<len(stocktoget):    
        stock = stocktoget[stockloop]
        
        ret_sub, err_message = quote_ctx.subscribe(stock, [SubType.K_DAY], subscribe_push=False)
        # 先订阅 K 线类型。订阅成功后 FutuOpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = quote_ctx.get_cur_kline(stock, 1000, SubType.K_DAY, AuType.QFQ)  # 获取港股00700最近2个 K 线数据
            if ret == RET_OK:
                data.to_pickle(f'{stock}.pkl')
            else:
                print('error:', data)
        else:
            print('subscription failed', err_message)
        stockrange+=1
        stockloop+=1
    
    count+=1
    stockloop=0
    print(count)
    print(stockloop)
    print(stockrange)
    quote_ctx.close()
    time.sleep(65)

# 关闭当条连接，FutuOpenD 会在1分钟后自动取消相应股票相应类型的订阅

# print(timetoloop)
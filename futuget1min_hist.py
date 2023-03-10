# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 03:37:04 2023

@author: user
"""

import pandas as pd
from futu import *
with open('hsi_weighting.txt', 'r') as f:
    stock_list = f.read().splitlines()

stock_list = ['HK.800000']
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
for stock in stock_list:
    templist = []
    ret, data, page_req_key = quote_ctx.request_history_kline(stock, start='2021-03-11', end='2023-03-10', ktype='K_1M', max_count=1000)  # 每页5个，请求第一页
    if ret == RET_OK:
        # print(data)
        templist.append(data)
        # print(data['code'][0])    # 取第一条的股票代码
        # print(data['close'].values.tolist())   # 第一页收盘价转为 list
    else:
        print('error:', data)
    while page_req_key != None:  # 请求后面的所有结果
        # print('*************************************')
        ret, data, page_req_key = quote_ctx.request_history_kline(stock, start='2021-03-11', end='2023-03-10', max_count=1000, ktype='K_1M', page_req_key=page_req_key) # 请求翻页后的数据
        if ret == RET_OK:
            # print(data)
            templist.append(data)
        else:
            print('error:', data)
    print('All pages are finished!')
    
    df = pd.concat(templist)
    df.to_pickle(f'{stock}_1min.pkl')
    print(f'{stock} done')
    
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
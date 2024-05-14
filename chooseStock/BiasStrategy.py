#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import os.path
import sys
from datetime import datetime
import pandas as pd 
import efinance as ef
from typing import Dict
import time
import random


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from stocks.getStockHis import get_db_stock_his
from stocks.getStockList import get_db_stock_list
from lib.mongoDB import bulk_insert

# 初始化变量
end_date = datetime.now().strftime('%Y%m%d')  # 获取当前日期，格式为YYYYMMDD
day_nums = 1  # 用于寻找交易信号的回溯天数
stock_num = 10  # 考虑交易的排名前几的股票数量
momentum_day = 20  # 计算动量评分所需的天数
ref_stock = 'sh000300'  # 用于定时计算的参考股票
N = 18  # 线性回归计算所需的天数
M = 600  # 计算Z-score所需的天数
score_threshold = 0.7  # 考虑进行交易的股票阈值
freq = 1


# def get_realtime_stock(stock_codes):
#     status = {stock_code: 0 for stock_code in stock_codes}
#     while len(stock_codes) != 0:
#         # 获取最新一个交易日的分钟级别股票行情数据
#         stocks_df: Dict[str, pd.DataFrame] = ef.stock.get_quote_history(
#             stock_codes, klt=freq)
#         print('---stocks_df',stocks_df)
#         for stock_code, df in stocks_df.items():
#             # 现在的时间
#             now = str(datetime.today()).split('.')[0]
#             # 将数据存储到 csv 文件中
#             df.to_csv(f'{stock_code}.csv', encoding='utf-8-sig', index=None)
#             print(f'已在 {now}, 将股票: {stock_code} 的行情数据存储到文件: {stock_code}.csv 中！')
#             if len(df) == status[stock_code]:
#                 # 移除已经收盘的股票代码
#                 stock_codes.remove(stock_code)
#                 print(f'股票 {stock_code} 已收盘！')
#             status[stock_code] = len(df)
#         if len(stock_codes) != 0:
#             print('暂停 60 秒')
#             random_number = random.randint(0, 60)       
#             time.sleep(random_number)
#         print('-'*10)
    

# 获取指数列表的函数
def get_index_list():
    # stocks = ak.stock_zt_pool_strong_em(date=end_date)  # 获取指定日期的涨停强势股票列表
    stocks = get_db_stock_list()   
    stock_codes = [stock['code'] for stock in stocks if 'ST' not in stock['name'] and not stock['code'].startswith('688') and not stock['code'].startswith('8')and not stock['code'].startswith('4')]
    print('----非ST的股票的只数---',len(stock_codes))
    return stock_codes

 
# 乖离因子（Bias Ratio）是一种技术指标，用于衡量股价与其移动平均线之间的偏离程度。它的计算方式是当前价格除以移动平均线的值，通常以百分比形式表示
# 计算动量评分的函数
def calculate_momentum_score(valid_data):
    biasN = 90  # 计算乖离因子所需的天数
    if len(valid_data) >= biasN:
        bias = np.array((valid_data.close / valid_data.close.rolling(biasN).mean())[-momentum_day:])  # 计算乖离因子
        relative_bias = bias / bias[0]  # 计算相对乖离因子
        coefficients = np.polyfit(np.arange(momentum_day), relative_bias, 1)  # 进行线性拟合
        score = coefficients[0]  # 提取斜率作为动量评分
        return score
    else:
        return None

# 获取排名前几的股票基于动量评分
def get_top_ranked_stocks(stock_pool):
    rank = []
    for stock in stock_pool:
        data = get_db_stock_his(stock)
        if data:
            valid_data = pd.DataFrame(data)  # 将列表转换为 DataFrame
            score = calculate_momentum_score(valid_data)
            if score is not None:
                rank.append([stock, score])
    rank.sort(key=lambda x: x[-1], reverse=True)  # 根据动量评分降序排序
    return rank[:stock_num]  # 返回排名前几的股票列表

def save_to_db(stocks):
    list = []
    for stock in stocks:
        data = {
            'code': stock[0],  
            'momentum_score': stock[1],  # 动量评分
            'timestamp': datetime.now()  
        }
        list.append(data)
    bulk_insert('stk_choose_bins',list)

# 主要交易函数
def my_trade():
    # get_realtime_stock(['301069','603032'])

    stock_pool = get_index_list()  # 获取指数列表
    top_ranked_stocks = get_top_ranked_stocks(stock_pool)  # 获取排名前几的股票列表
    save_to_db(top_ranked_stocks)
    codes = [stock[0] for stock in top_ranked_stocks ]
    print('----',codes)
    # get_realtime_stock(codes)
    if top_ranked_stocks:
        top_stock = top_ranked_stocks[0]
        print(top_ranked_stocks)
        print('今日排名第一的股票: {} ({:.3f})'.format(top_stock[0], top_stock[1]))  # 打印排名第一的股票信息

if __name__ == '__main__':
    my_trade()

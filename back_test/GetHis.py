import akshare as ak
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient, UpdateOne

import os.path
import sys
#乖离因子（Bias Ratio）是一种技术指标，用于衡量股价与其移动平均线之间的偏离程度。它的计算方式是当前价格除以移动平均线的值，通常以百分比形式表示
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from  lib.mongoDB import STOCK_DB
# 初始化变量
end_date = datetime.now().strftime('%Y%m%d')
# 是否检查存在数据
need_check_exist = True
# 批量插入大小
batch_size = 5

 

# 获取股票列表的函数
def get_index_list():
    stocks = ak.stock_info_a_code_name()
    stock_codes = stocks.loc[(~stocks["code"].str.startswith("ST")), "code"].tolist()
    print(f'获取股票列表成功,共{len(stock_codes)} ')
    return stock_codes[1001:]

# 获取历史数据的函数
def get_historical_data(code, period, adjust):
    try:
        data = ak.stock_zh_a_hist(symbol=code, period=period, start_date="19910101", end_date='20240424', adjust=adjust).iloc[:, :11]
        if not data.empty:
            data.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'amplitude', 'change', 'changeAmount', 'turnoverRate']
            data['date'] = pd.to_datetime(data['date'])
            data.index = pd.to_datetime(data['date'])
            data = data.query('volume !=0')
            data['period'] = period
            data['adjust'] = adjust
            data['code'] = code  # 添加股票代码字段
            print(f"获取{code}{period}{adjust} 数据成功")
            return data
        else:
            print(f"{code} 数据为空")
            return None
    except Exception as e:
        print(f"{code} 数据时出错：{str(e)}")
        return None

# 批量插入数据到数据库
def bulk_insert(collection_name, data_list):
    if data_list:
        try:
            STOCK_DB[collection_name].insert_many(data_list)
            print(f"成功插入 {collection_name} 数据")
        except Exception as e:
            print(f"插入 {collection_name} 数据时出错：{str(e)}")

# 获取历史数据并插入数据库
def get_top_ranked_stocks(stock_pool):
    bulk_operations = {}
    for stock in stock_pool:
        for period in ['daily', 'weekly', 'monthly']:
            for adjust in ['', 'qfq', 'hfq']:
                try:
                    data = get_historical_data(stock, period, adjust)
                    if data is not None:
                        collection_name = f"stk_{stock}"
                        if collection_name not in bulk_operations:
                            bulk_operations[collection_name] = []
                        bulk_operations[collection_name].append(data)
                except Exception as e:
                    print(f"获取 {stock} {period} {adjust} 数据时出错：{str(e)}")

    # 执行批量插入
    for collection_name, data_list in bulk_operations.items():
        merged_data = pd.concat(data_list)
        bulk_insert(collection_name, merged_data.to_dict(orient='records'))

def get_his_data():
    stock_pool = get_index_list()
    for i in range(0, len(stock_pool), batch_size):
        batch_stocks = stock_pool[i:i+batch_size]
        get_top_ranked_stocks(batch_stocks)

if __name__ == '__main__':
    get_his_data()

import akshare as ak
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import os.path
import sys
# 加载其他模块
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from lib.mongoDB import STOCK_DB, bulk_insert
from lib.enums import PeriodEnum, AdjustEnum
from stocks.getStockList import get_db_stock_list


# 获取不同股票代码的最新日期
def get_latest_date_from_db(code):
    collection_name = f"stk_{code}"
    collection = STOCK_DB[collection_name]
    latest_doc = collection.find_one(sort=[("date", -1)])
    if latest_doc:
        return latest_doc["date"].strftime('%Y%m%d')
    else:
        return '19900715'

# 初始化变量
end_date = datetime.now().strftime('%Y%m%d')
# 批量插入大小
batch_size = 5

# 获取历史数据
def get_historical_data(code, period: PeriodEnum, adjust: AdjustEnum, start_date):
    try:
        period_value = period.value
        adjust_value = adjust.value
        data = ak.stock_zh_a_hist(symbol=code, period=period_value, start_date=start_date, end_date=end_date, adjust=adjust_value).iloc[:, :11].copy()
        if not data.empty:
            data.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'amplitude', 'change', 'changeAmount', 'turnoverRate']
            data['date'] = pd.to_datetime(data['date'])
            data.index = pd.to_datetime(data['date'])
            data = data.query('volume !=0')
            data['period'] = period_value
            data['adjust'] = adjust_value
            data['code'] = code  # 添加股票代码字段
            print(f"获取{code}时间：{start_date}-{end_date}周期：{period_value}复权方式：{adjust_value} 数据成功")
            return data
        else:
            print(f"{code} 数据为空")
            return None
    except Exception as e:
        print(f"{code} 数据时出错：{str(e)}")
        return None

# 批量获取历史数据并插入数据库
def fetch_and_insert_stock_data(stock_pool):
    bulk_operations = {}
    for stock in stock_pool:
        latest_date = get_latest_date_from_db(stock)
        if latest_date == end_date:
            print(f"{stock} 已经是最新数据，无需更新")
            continue
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(get_historical_data, stock, period, adjust, latest_date): (stock, period, adjust, latest_date) for period in [PeriodEnum.daily, PeriodEnum.weekly, PeriodEnum.monthly]
                       for adjust in [AdjustEnum.NOT_ADJUST, AdjustEnum.QFQ, AdjustEnum.HFQ]}
            for future in futures:
                stock, period, adjust, latest_date = futures[future]  # 解包future对象
                try:
                    data = future.result()
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
# 获取历史数据
def store_his_data():
    stock_pool = get_db_stock_list()
    stock_pool = [item['code'] for item in stock_pool]
    for i in range(0, len(stock_pool), batch_size):
        batch_stocks = stock_pool[i:i+batch_size]
        fetch_and_insert_stock_data(batch_stocks)

if __name__ == '__main__':
    store_his_data()

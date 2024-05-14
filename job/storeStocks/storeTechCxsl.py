import akshare as ak
from datetime import date

import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from lib.mongoDB import bulk_delete, bulk_insert
#持续缩量

def get_cxsl_stocks():
    try:
        stocks = ak.stock_rank_cxsl_ths().iloc[:, :10] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None
# 持续放量
def get_cxfl_stocks():
    try:
        stocks = ak.stock_rank_cxfl_ths().iloc[:, :10] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None

def translate_to_english(individual_info,type):
    # Dictionary for translating Chinese keys to English
    translate_dict = {
        "股票代码": "code",
        "股票简称": "name",
        "最新价": "price",
        "涨跌幅": "changeRate",
        "成交量": "volume",
        "所属行业": "industry",
        "累计换手率": "turnover",
        "基准日成交量": "benchmarkVolume",
        "阶段涨跌幅":"stageRate"
    }
    if(type == 'cxsl'):
        translate_dict['缩量天数']='nums'
    else:
        translate_dict['放量天数']='nums'
    formatted_info = {}
    for chinese_key, value in individual_info.items():
        if chinese_key != "序号":  # Exclude the serial number field
            english_key = translate_dict.get(chinese_key, chinese_key)
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            formatted_info[english_key] = value
    return formatted_info

def store_tech_cxsl_stocks():
    stock_list = get_cxsl_stocks()
    if stock_list is not None:
        cxsl_list = []
        for item in stock_list:
            translated_item = translate_to_english(item,'cxsl')
            cxsl_list.append(translated_item)
        
        # Insert translated data into MongoDB
        bulk_insert("stock_tech_cxsl", cxsl_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")
def store_tech_cxfl_stocks():
    stock_list = get_cxfl_stocks()
    if stock_list is not None:
        cxfl_list = []
        for item in stock_list:
            translated_item = translate_to_english(item,'csfl')
            cxfl_list.append(translated_item)
        # Insert translated data into MongoDB
        bulk_insert("stock_tech_cxfl", cxfl_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")

if __name__ == '__main__':
    bulk_delete('stock_tech_cxsl')
    bulk_delete('stock_tech_cxfl')
    store_tech_cxsl_stocks()
    store_tech_cxfl_stocks()

import akshare as ak
from datetime import date

import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from lib.mongoDB import bulk_delete, bulk_insert

# 连续上涨
def get_lxsz_stocks():
    try:
        stocks = ak.stock_rank_lxsz_ths().iloc[:, :10] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None
# 连续下跌
def stock_rank_lxxd_ths():
    try:
        stocks = ak.stock_rank_lxxd_ths().iloc[:, :10] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None

def translate_to_english(individual_info):
    # Dictionary for translating Chinese keys to English
    translate_dict = {
        "股票代码": "code",
        "股票简称": "name",
        "收盘价": "close",
        "最高价": "high",
        "最低价": "low",
        "所属行业": "industry",
        "累计换手率": "turnover",
        "连涨天数": "nums",
        "连续涨跌幅":"stageRate"
    }
    formatted_info = {}
    for chinese_key, value in individual_info.items():
        if chinese_key != "序号":  # Exclude the serial number field
            english_key = translate_dict.get(chinese_key, chinese_key)
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            formatted_info[english_key] = value
    return formatted_info

#持续缩量
def store_tech_lxsz_stocks():
    stock_list = get_lxsz_stocks()
    if stock_list is not None:
        cxsl_list = []
        for item in stock_list:
            translated_item = translate_to_english(item)
            cxsl_list.append(translated_item)
        
        # Insert translated data into MongoDB
        bulk_insert("stock_tech_lxsz", cxsl_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")
def store_tech_lxxd_stocks():
    stock_list = stock_rank_lxxd_ths()
    if stock_list is not None:
        cxfl_list = []
        for item in stock_list:
            translated_item = translate_to_english(item)
            cxfl_list.append(translated_item)
        # Insert translated data into MongoDB
        bulk_insert("stock_tech_lxxd", cxfl_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")

if __name__ == '__main__':
    bulk_delete('stock_tech_lxsz')
    bulk_delete('stock_tech_lxxd')

    store_tech_lxsz_stocks()
    store_tech_lxxd_stocks()

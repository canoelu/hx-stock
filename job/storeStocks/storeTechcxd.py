import akshare as ak
from datetime import date
import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from lib.mongoDB import bulk_delete, bulk_insert

def get_cxg_stocks(symbol):
    try:
        stocks = ak.stock_rank_cxg_ths(symbol).iloc[:, :8] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None

def stock_cxd_ths(symbol):
    try:
        stocks = ak.stock_rank_cxd_ths(symbol).iloc[:, :8] 
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to retrieve stock information: {e}")
        return None

def translate_to_english(individual_info,symbol):
    translate_dict = {
        "股票代码": "code",
        "股票简称": "name",
        "换手率": "turnover",
        "涨跌幅": "changeRate",
        "最新价": "price",
        "前期低点": "preLow",
        "前期低点日期": "preLowDate",
        "前期高点": "preHigh",
        "前期高点日期": "preHighDate"
    }
    symbol_dict = {
    "创月新高": "monthHigh",
    "半年新高": "halfHigh",
    "一年新高": "yearHigh",
    "历史新高": "hisHigh",
    "创月新低": "monthLow",
    "半年新低": "halfLow",
    "一年新低": "yearLow",
    "历史新低": "hisLow"
    }
    formatted_info = {
        "symbol":symbol_dict[symbol]
    }
    for chinese_key, value in individual_info.items():
        if chinese_key != "序号":  # Exclude the serial number field
            english_key = translate_dict.get(chinese_key, chinese_key)
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            formatted_info[english_key] = value
    return formatted_info

def store_tech_cxg_stocks(symbol):
    stock_list = get_cxg_stocks(symbol)
    if stock_list is not None:
        cxg_list = []
        for item in stock_list:
            translated_item = translate_to_english(item,symbol)
            cxg_list.append(translated_item)
        bulk_insert("stock_tech_cxg", cxg_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")

def store_tech_cxd_stocks(symbol):
    stock_list = stock_cxd_ths(symbol)
    if stock_list is not None:
        cxd_list = []
        for item in stock_list:
            translated_item = translate_to_english(item,symbol)
            cxd_list.append(translated_item)
        bulk_insert("stock_tech_cxd", cxd_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")

def store_tech_cxdg_stocks():
    for symbol_choice in {"创月新高", "半年新高", "一年新高", "历史新高","创月新低", "半年新低", "一年新低", "历史新低"}:
        if "新高" in symbol_choice:
            store_tech_cxg_stocks(symbol_choice)
        elif "新低" in symbol_choice:
            store_tech_cxd_stocks(symbol_choice)
    else:
        print("Invalid symbol choice.")
    
if __name__ == '__main__':
    bulk_delete('stock_tech_cxd')
    bulk_delete('stock_tech_cxg')
    store_tech_cxdg_stocks()
    

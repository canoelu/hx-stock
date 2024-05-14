import akshare as ak
from datetime import date
import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from lib.mongoDB import bulk_delete, bulk_insert

def get_xstp_stocks(symbol):
    try:
        stocks = ak.stock_rank_xstp_ths(symbol).iloc[:, :8] 
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
        "成交量": "volume",
        "所属行业": "industry",
        "成交额": "amount",

    }
    symbol_dict = {
        "5日均线": "5avg",
        "10日均线": "10avg",
        "20日均线": "20avg",
        "30日均线": "30avg",
        "60日均线": "60avg",
        "90日均线": "90avg",
        "250日均线": "250avg",
        "500日均线": "500avg"
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

def store_xstp_stocks(symbol):
    stock_list = get_xstp_stocks(symbol)
    if stock_list is not None:
        xstp_list = []
        for item in stock_list:
            translated_item = translate_to_english(item,symbol)
            xstp_list.append(translated_item)
        bulk_insert("stock_tech_xstp", xstp_list)
        print("Translation and data storage successful!")
    else:
        print("Failed to retrieve stock information. Unable to translate and store.")

 
def store_tech_xstp_stocks():
    for symbol_choice in {"5日均线", "10日均线", "20日均线", "30日均线","60日均线", "90日均线", "250日均线", "500日均线"}:
        store_xstp_stocks(symbol_choice)
    else:
        print("Invalid symbol choice.")
    
if __name__ == '__main__':
    bulk_delete('stock_tech_xstp')
    store_tech_xstp_stocks()
    

import akshare as ak
from datetime import  date
import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from lib.mongoDB import bulk_delete, bulk_insert

# 险资举牌
def get_rank_xzjp_list():
    try:
        stocks = ak.stock_rank_xzjp_ths().iloc[:, :15] 
        # DataFrame 转为列表
        return stocks.to_dict(orient="records")
    except Exception as e:
        print(f"获取个股信息失败：{e}")
        return None

def translate_to_english(individual_info):
    # 中英文对照字典
    translate_dict = {
        "股票代码": "code",
        "股票简称": "name",
        "现价": "price",
        "涨跌幅": "changeRate",
        "举牌公告日": "announcementDate",
        "举牌方": "tenderOfferor",
        "增持数量": "increaseQuantity",
        "交易均价": "averagePrice",
        "增持数量占总股本比例": "increasePercent",
        "变动后持股比例": "percent",
        "变动后持股总数": "total"
    }
    formatted_info = {
    }
    for chinese_key, value in individual_info.items():
        if chinese_key != "序号":  # 排除序号字段
            english_key = translate_dict.get(chinese_key, chinese_key)
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            formatted_info[english_key] = value
    return formatted_info


 
# 主逻辑
def store_tech_xzjp_stocks():
    stock_list = get_rank_xzjp_list()
    if stock_list is not None:
        # 使用翻译API进行翻译并插入MongoDB
        translated_data_list = []
        for item in stock_list:
            translated_item = translate_to_english(item)
            translated_data_list.append(translated_item)
        
        # 将翻译后的数据插入MongoDB
        bulk_insert("stock_tech_xzjp", translated_data_list)
        print("翻译并存储数据成功！")
    else:
        print("获取个股信息失败，无法进行翻译和存储。")

if __name__ == '__main__':
    bulk_delete('stock_tech_xzjp')
    store_tech_xzjp_stocks()

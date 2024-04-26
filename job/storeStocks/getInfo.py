import akshare as ak
from datetime import datetime
from pymongo import MongoClient
import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from  lib.mongoDB import STOCK_DB

# 初始化变量
end_date = datetime.now().strftime('%Y%m%d')
# 是否检查存在数据
need_check_exist = True

# 缓存字典
cacheList = {}
cache = {}

# 获取股票列表的函数
def get_stock_list():
    global cacheList
    # 如果缓存中已经有该查询结果，则直接返回缓存中的数据
    if end_date in cacheList:
        print('使用的缓存')
        return cacheList[end_date]
    stocks = ak.stock_info_a_code_name()
    stock_codes = stocks.loc[(~stocks["code"].str.startswith("ST")), "code"].tolist()
    print(f'获取股票列表成功,共{len(stock_codes)} ')
    cacheList[end_date] = stock_codes
    return stock_codes

# 获取个股信息
def get_individual_info(code):
    try:
        individual_info = ak.stock_individual_info_em(symbol=code).iloc[:, :2]
        print(f"原始个股信息{code}：", individual_info)
        return individual_info
    except Exception as e:
        print(f"获取个股信息失败{code}：{e}")
        return None

def translate_to_english(individual_info):
    # 转换 DataFrame 为字典列表
    individual_info_dict = individual_info.to_dict(orient="records")
    
    # 中英文对照字典
    translate_dict = {
        "总市值": "totalValue",
        "流通市值": "circulatingValue",
        "行业": "industry",
        "上市时间": "listingDate",
        "股票代码": "code",
        "股票简称": "name",
        "总股本": "totalEquity",
        "流通股": "circulatingEquity"
    }
    formatted_info = {}
    for item in individual_info_dict:
        chinese_key = item["item"]
        english_key = translate_dict.get(chinese_key, chinese_key)
        value = item["value"]
        formatted_info[english_key] = value
    return formatted_info



# 检查是否文档中已经存在当前个股
def check_exist_in_mongodb(collection_name, stock_code):
    collection = STOCK_DB[collection_name]
    existing_doc = collection.find_one({"code": stock_code})
    return existing_doc is not None

# 将数据插入到 MongoDB 中
def insert_into_mongodb(collection_name, data):
    collection = STOCK_DB[collection_name]
    collection.insert_many(data)

# 主逻辑
def get_all_stock_base_info():
    global cache
    stock_list = get_stock_list()
    all_stock_info = []
    # 限制每次访问个股信息的数量为10
    for i in range(0, len(stock_list), 10):
        batch_stock_list = stock_list[i:i+10]
        for stock_code in batch_stock_list:
            # 检查文档是否已经存在当前个股
            if need_check_exist and check_exist_in_mongodb("stock_base", stock_code):
                print(f"股票 {stock_code} 已存在于 MongoDB 中，跳过插入。")
                continue
            # 先尝试从缓存中获取个股信息
            individual_info = cache.get(stock_code)
            if not individual_info:
                # 如果缓存中没有，就从 ak.stock_individual_info_em 获取个股信息
                individual_info = get_individual_info(stock_code)
                # 转换为英文数据
                individual_info = translate_to_english(individual_info)
                # 更新缓存
                cache[stock_code] = individual_info
            all_stock_info.append(individual_info)
    # 将获取到的所有股票信息插入到 MongoDB 中
    insert_into_mongodb("stock_base", all_stock_info)

if __name__ == '__main__':
    get_all_stock_base_info()

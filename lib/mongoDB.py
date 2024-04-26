
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
STOCK_DB = client.stock

# 批量插入数据到数据库
def bulk_insert(collection_name, data_list):
    if data_list:
        try:
            STOCK_DB[collection_name].insert_many(data_list)
            print(f"成功插入 {collection_name} 数据")
        except Exception as e:
            print(f"插入 {collection_name} 数据时出错：{str(e)}")
            
# 检查数据库中是否存在文档
def document_exists_in_db(collection_name, start_date, end_date):
    collection = STOCK_DB[collection_name]
    query = {"date": {"$gte": start_date, "$lte": end_date}}
    result = collection.find_one(query)
    return result is not None
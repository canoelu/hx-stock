
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
STOCK_DB = client.stock

def bulk_delete(collection_name):
    collection = STOCK_DB[collection_name]
    collection.delete_many({})

# 批量插入数据到数据库
def bulk_insert(collection_name, data):
    if not isinstance(data, list):
        raise TypeError("数据必须是一个字典列表。")
    try:
        collection = STOCK_DB[collection_name]
        collection.insert_many(data)
        print(f"成功插入 {len(data)} 条数据到集合 {collection_name} 中。")
    except Exception as e:
        print(f"插入数据到集合 {collection_name} 失败：{e}")
            
# 检查数据库中是否存在文档
def document_exists_in_db(collection_name, start_date, end_date):
    collection = STOCK_DB[collection_name]
    query = {"date": {"$gte": start_date, "$lte": end_date}}
    result = collection.find_one(query)
    return result is not None

# 检查是否文档中已经存在当前个股
def check_exist_in_mongodb(collection_name, stock_code):
    collection = STOCK_DB[collection_name]
    existing_doc = collection.find_one({"code": stock_code})
    return existing_doc is not None
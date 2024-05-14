
from lib.mongoDB import STOCK_DB

def get_db_stock_list():
    try:
        collection_name = "stock_base"
        collection = STOCK_DB[collection_name]
        # 否则进行数据库查询
        query = {}
        result = list(collection.find(query, {'_id': False}))
        return result
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        return []

         


# main函数入口
from lib.mongoDB import STOCK_DB


if __name__ == '__main__':
    collection_name = f"stk_0000001"
    collection = STOCK_DB[collection_name]()

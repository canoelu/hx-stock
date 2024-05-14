from fastapi import APIRouter, HTTPException
import pymongo
from lib.mongoDB import STOCK_DB
 
router = APIRouter()


async def get_page_data(collection_name, query, page, limit, sort_field=None, sort_order=None):
    """
    辅助函数，用于从数据库获取股票数据并缓存结果。

    参数:
    - collection_name: MongoDB集合名称。
    - query: 查询条件。
    - page: 页码。
    - limit: 每页项目数。
    - sort_field: 字段名称，用于排序（可选）。
    - sort_order: 排序顺序（可选）。

    返回:
    - 一个包含(stock_list, total_count)的元组。
    """
    # 获取集合
    collection = STOCK_DB[collection_name]

 

    # 计算需要跳过的文档数量
    skip_count = (page - 1) * limit

    try:
        # 获取总条数
        total = collection.count_documents(query)
        
        # 添加排序逻辑
        sort_criteria = None
        if sort_field and sort_order:
            sort_order = pymongo.ASCENDING if sort_order == 'ascend' else pymongo.DESCENDING
            sort_criteria = [(sort_field, sort_order)]
        
        # 查询股票列表并进行排序
        stocks = collection.find(query, {'_id': False}).skip(skip_count).limit(limit)
        if sort_criteria:
            stocks = stocks.sort(sort_criteria)
        
        stock_list = [stock for stock in stocks]  # 转换为列表
    except Exception as e:
        raise HTTPException(status_code=500, detail="内部服务器错误")


    return stock_list, total

def format_response(data=None,total=0,page=1,pageSize=10,code: int=0, message: str='success'):
    """
    格式化响应数据
    """
    return {
        'code': code,
        'message': message,
        'result': {
            "items":data,
            "page":page,
            "pageSize":pageSize,
            "total":total
        }
    }

from fastapi import APIRouter, Query,HTTPException
from lib.mongoDB import STOCK_DB
from routers.common import format_response, get_page_data
import re
from pydantic import BaseModel

router = APIRouter()
 
collection=STOCK_DB['stock_base']

# 辅助函数
def change_status(code: str, field: str, status: bool):
    # 检查是否存在相应股票
    stock = collection.find_one({"code": code})
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # 更新股票状态
    collection.update_one({"code": code}, {"$set": {field: status}})
    # action = "blacklisted" if status else "unblacklisted"
    return   {
        'code': 0,
        'message': 'success',
        'result': True
    }
 
@router.get('/stocks/all')
async def get_stocks(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
    type: str = None
):
    # Build the query
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
         # 根据 type 过滤黑名单或关注列表
    if type == "black":
        query["blacklisted"] = True
    elif type == "attention":
        query["attentioned"] = True

    stock_list, total =await get_page_data("stock_base", query, page, pageSize, field, order)
    return format_response(stock_list, total,page,pageSize)

class Item(BaseModel):
    type: str
@router.put("/stocks/{code}/update")
async def change_stock_status(code: str, item:Item):
    print('code',code)
    print('item',item)
    if item.type == "black":
        return change_status(code, "blacklisted", True)
    elif item.type == "unblack":
        return change_status(code, "blacklisted", False)
    elif item.type == "attention":
        return change_status(code, "attentioned", True)
    elif item.type == "unattention":
        return change_status(code, "attentioned", False)
    else:
        raise HTTPException(status_code=400, detail="Invalid status type. Use 'blacklist' or 'unblacklist'.")

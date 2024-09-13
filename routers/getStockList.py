from fastapi import APIRouter, Query, HTTPException
from lib.mongoDB import STOCK_DB
from routers.common import format_response, get_page_data
import re
from pydantic import BaseModel, Field
from typing import List
from datetime import date


router = APIRouter()

collection = STOCK_DB['stock_base']
replay_collection = STOCK_DB['stock_replay']

# 辅助函数
def change_status(code: str, field: str, status: bool):
    # 检查是否存在相应股票
    stock = collection.find_one({"code": code})
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # 更新股票状态
    collection.update_one({"code": code}, {"$set": {field: status}})
    return {
        'code': 0,
        'message': 'success',
        'result': True
    }

@router.get('/stocks/all')
async def get_stocks(
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str = None,
    code: str = None,
    name: str = None,
    type: str = None
):
    # 构建查询条件
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

    stock_list, total = await get_page_data("stock_base", query, page, pageSize, field, order)
    return format_response(stock_list, total, page, pageSize)

# Pydantic 模型
class Item(BaseModel):
    type: str

# 更新股票状态接口
@router.put("/stocks/{code}/update")
async def change_stock_status(code: str, item: Item):
    valid_types = ["black", "unblack", "attention", "unattention"]
    
    # 检查type是否为有效的选项
    if item.type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status type. Use one of {valid_types}."
        )

    # 根据不同类型调用辅助函数更新状态
    if item.type == "black":
        return change_status(code, "blacklisted", True)
    elif item.type == "unblack":
        return change_status(code, "blacklisted", False)
    elif item.type == "attention":
        return change_status(code, "attentioned", True)
    elif item.type == "unattention":
        return change_status(code, "attentioned", False)


# 定义单只股票的数据结构
class StockData(BaseModel):
    latest: float = Field(..., description="最新价")
    avg_price: float = Field(..., description="平均价")
    increase_pct: float = Field(..., description="涨跌幅")
    increase: float = Field(..., description="涨跌额")
    total_volume: int = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")
    turnover: float = Field(..., description="换手率")
    volume_ratio: float = Field(..., description="量比")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    open: float = Field(..., description="开盘价")
    prev_close: float = Field(..., description="昨收价")
    limit_up: float = Field(..., description="涨停价")
    limit_down: float = Field(..., description="跌停价")
    buy_vol: int = Field(..., description="买入量")
    sell_vol: int = Field(..., description="卖出量")
    volPrice: str = Field(..., description="成交价格概况")
    unitVol: str = Field(..., description="买卖能量对比")
    buyPower: str = Field(..., description="买入能量")
    sellPower: str = Field(..., description="卖出能量")
    buyAndSell: str = Field(..., description="买卖差异")
    amplitude: float = Field(..., description="振幅")
# 定义复盘数据模型
class StockReplay(BaseModel):
    # date: date = Field(..., description="复盘日期")
    date: str = Field(..., description="复盘日期 (YYYY-MM-DD 格式)")

    stocks: List[StockData] = Field(..., description="股票列表")
    
@router.post('/stocks/replay/save')
async def save_stock_replay(replay_data: StockReplay):
    stocks_as_dict = [stock.dict() for stock in replay_data.stocks]

    # 查找是否已经存在相同日期的复盘数据
    existing_replay = replay_collection.find_one({"date": replay_data.date})
    
    if existing_replay:
        # 如果存在相同日期的复盘数据，则更新现有的股票列表
        result = replay_collection.update_one(
            {"date": replay_data.date},
            {
                "$set": {
                    "stocks": stocks_as_dict  # 更新股票列表
                }
            }
        )
        message = "Replay data updated successfully"
    else:
        # 如果该日期的复盘数据不存在，则插入新数据
        result = replay_collection.insert_one({
            "date": replay_data.date,
            "stocks": replay_data.stocks
        })
        message = "Replay data inserted successfully"
    
    return {
        "code": 0,
        "message": message,
        "result": replay_data.dict()
    }
    
@router.get('/replay/{date}')
async def get_stock_replay(date: str):
    # 查找对应日期的复盘数据
    replay_data = replay_collection.find_one({"date": date})

    if not replay_data:
        raise HTTPException(status_code=404, detail="Replay data not found for the given date")

    return {
        "code": 0,
        "message": "Replay data retrieved successfully",
        "result": replay_data
    }
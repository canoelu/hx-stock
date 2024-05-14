#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from datetime import datetime
from lib.enums import PeriodEnum,AdjustEnum
from routers.common import format_response
from stocks.getStockHis import get_db_stock_his

router = APIRouter()

# 创建一个缓存字典
cache = {}

@router.get('/k/{code}')
async def get_stock_kLine(
    code: str, 
    period: PeriodEnum = PeriodEnum.daily, 
    adjust: AdjustEnum = AdjustEnum.NOT_ADJUST, 
    start_time: str = '2023-01-01', 
    end_time: str = ''
):
    """
    获取股票 k 线数据。

    Parameters:
    - code: 股票代码
    - period: 数据周期（daily, weekly, monthly）默认daily
    - adjust: 调整方式（'', qfq, hfq）默认''
    - start_time: 开始时间（YYYY-MM-DD）,默认从2023-01-01
    - end_time: 结束时间（YYYY-MM-DD）

    Returns:{
        'code':0,
        'message':'success',
        "data": result
    }
    - 股票数据列表
    """
    try:
        start_date = datetime.strptime(start_time, '%Y-%m-%d') if start_time else None
        end_date = datetime.strptime(end_time, '%Y-%m-%d') if end_time else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be later than end date.")

    # 构造查询条件的哈希键
    cache_key = (code, period.value, adjust.value, start_date, end_date)

    # 如果缓存中已经有该查询结果，则直接返回缓存中的数据
    if cache_key in cache:
        print(f'{code}使用的缓存')
        return {"data": cache[cache_key]}

    # 否则进行数据库查询
    result=get_db_stock_his( code, period, adjust, start_time, end_time)

    # 将查询结果存入缓存
    cache[cache_key] = result

    # 返回查询结果
    return format_response(result)

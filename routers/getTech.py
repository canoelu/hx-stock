from fastapi import APIRouter, Query
from lib.enums import CxdEnum, CxgEnum, XstpEnum
from routers.common import get_page_data,format_response
import re

router = APIRouter()


@router.get('/tech/cxd')
async def getTechCxd(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
    symbol:CxdEnum = None

):
    """
    获取创新低的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）
    - sort_field: 字段名称，用于排序（可选）。
    - sort_order: 排序顺序（可选）。
    - symbol: 根据不同选项筛选数据，可选值为 "monthLow", "halfLow", "yearLow", "hisLow" (可选)


    返回:
    - 创新低的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    if symbol:
        query["symbol"] = symbol.value
    stock_list, total =await get_page_data("stock_tech_cxd", query, page, limit, field, order)
    return format_response(stock_list, total,page,limit)




@router.get('/tech/cxg')
async def getTechCxg(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
    symbol:CxgEnum = None

):
    """
    获取创新高的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）
    - sort_field: 字段名称，用于排序（可选）。
    - sort_order: 排序顺序（可选）。
    - symbol: 根据不同选项筛选数据，可选值为 "monthHigh", "halfHigh", "yearHigh", "hisHigh" (可选)


    返回:
    - 创新高的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    if symbol:
        query["symbol"] = symbol.value
    stock_list, total =await get_page_data("stock_tech_cxg", query, page, limit, field, order)
    return format_response(stock_list, total,page,limit)



@router.get('/tech/cxfl')
async def getTechCxfl(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
):
    """
    获取持续放量的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）
    - sort_field: 字段名称，用于排序（可选）。
    - sort_order: 排序顺序（可选）。
    - symbol: 根据不同选项筛选数据，可选值为 "monthHigh", "halfHigh", "yearHigh", "hisHigh" (可选)


    返回:
    - 持续放量的股票技术数据
    """
    # Build the query
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    stock_list, total =await get_page_data("stock_tech_cxfl", query, page, limit, field, order)
    return format_response(stock_list, total)



@router.get('/tech/cxsl')
async def getTechCxsl(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
):
    """
    获取持续缩量的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）
    - sort_field: 字段名称，用于排序（可选）。
    - sort_order: 排序顺序（可选）。
    - symbol: 根据不同选项筛选数据，可选值为 "monthHigh", "halfHigh", "yearHigh", "hisHigh" (可选)


    返回:
    - 持续缩量的股票技术数据
    """
    # Build the query
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    stock_list, total =await get_page_data("stock_tech_cxsl", query, page, limit, field, order)
    return format_response(stock_list, total)



@router.get('/tech/ljqs')
async def getTechLjqs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None
):
    """
    获取量价齐升的股票技术数据。

    
    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - field: 字段名称，用于排序。
    - order: 排序顺序，可选值为 'ascend', 'descend'。
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）

    返回:
    - 量价齐升的股票技术数据和总条数
    """
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
     
    stock_list, total =await get_page_data("stock_tech_ljqs", query, page, limit, field, order)

    return format_response(stock_list, total,page,limit)



@router.get('/tech/lxsz')
async def getTechLxsz(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None
):
    """
    获取连续上涨的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）

    返回:
    - 连续上涨的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    stock_list, total =await get_page_data("stock_tech_lxsz", query, page, limit, field, order)

    return format_response(stock_list, total,page,limit)


@router.get('/tech/lxxd')
async def getTechLxxd(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None
):
    """
    获取 连续下跌的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）

    返回:
    - 连续下跌的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    stock_list, total =await get_page_data("stock_tech_lxxd", query, page, limit, field, order)

    return format_response(stock_list, total,page,limit)


@router.get('/tech/xzjp')
async def getTechXzjp(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None
):
    """
    获取险资举牌的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）

    返回:
    - 险资举牌 的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    stock_list, total =await get_page_data("stock_tech_xzjp", query, page, limit, field, order)

    return format_response(stock_list, total,page,limit)


@router.get('/tech/xstp')
async def getTechXstp(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None,
    symbol:XstpEnum = None

):
    """
    获取向上突破的股票技术数据。

    参数:
    - page: 页码（默认 1，必须大于等于 1）
    - limit: 每页项目数（默认 10，必须在 1 到 100 之间）
    - code: 股票代码进行模糊搜索（可选）
    - name: 股票名称进行模糊搜索（可选）

    返回:
    - 向上突破的股票技术数据
    """
    # 构建查询条件
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}
    if symbol:
        query["symbol"] = symbol.value
    stock_list, total =await get_page_data("stock_tech_xstp", query, page, limit, field, order)

    return format_response(stock_list, total,page,limit)
 
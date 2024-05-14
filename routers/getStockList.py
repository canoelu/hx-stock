from fastapi import APIRouter, Query
from routers.common import format_response, get_page_data
import re

router = APIRouter()
 
@router.get('/stocks/all')
async def get_stocks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    field: str = None,
    order: str =None,
    code: str = None,
    name: str = None
):
    # Build the query
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}

    stock_list, total =await get_page_data("stock_base", query, page, limit, field, order)
    return format_response(stock_list, total,page,limit)

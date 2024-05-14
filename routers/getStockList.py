from fastapi import APIRouter, HTTPException, Query
from lib.mongoDB import STOCK_DB
from routers.common import format_response
import re

router = APIRouter()




collection_name = "stock_base"
collection = STOCK_DB[collection_name]

# Create a cache dictionary
cache = {}

@router.get('/stocks/all')
async def get_stocks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    code: str = None,
    name: str = None
):
    # Check if the query parameters are in the cache
    cache_key = (page, limit, code, name)
    if cache_key in cache:
        print("Using cached data for stocks")
        return format_response(cache[cache_key])

    # Calculate the number of documents to skip
    skip_count = (page - 1) * limit

    # Build the query
    query = {}
    if code:
        query["code"] = {"$regex": re.compile(re.escape(code), re.IGNORECASE)}
    if name:
        query["name"] = {"$regex": re.compile(re.escape(name), re.IGNORECASE)}

    # Query the stock list
    try:
        total = collection.count_documents(query)

        stocks = collection.find(query, {'_id': False}).skip(skip_count).limit(limit)
        stock_list = [stock for stock in stocks]  # Convert to list
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    # Store the result in the cache
    cache[cache_key] = stock_list

    return format_response(stock_list,total)

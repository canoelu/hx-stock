
import akshare as ak
from datetime import datetime
from lib.mongoDB import STOCK_DB
from lib.enums import PeriodEnum,AdjustEnum

def get_stock_his(
    code: str, 
    period: PeriodEnum = PeriodEnum.daily, 
    adjust: AdjustEnum = AdjustEnum.NOT_ADJUST, 
    start_time: str = '20230101', 
    end_time: str = ''
):
    """
    获取股票历史数据。

    Parameters:
    - code: 股票代码
    - period: 数据周期（daily, weekly, monthly）默认daily
    - adjust: 调整方式（'', qfq, hfq）默认''
    - start_time: 开始时间（YYYY-MM-DD）,默认从20230101
    - end_time: 结束时间（YYYY-MM-DD）

    Returns:
    - 股票数据列表
    """
    print('code', code)
    collection_name = f"stk_{code}"
    collection = STOCK_DB[collection_name]

    start_date = datetime.strptime(start_time, '%Y-%m-%d') if start_time else None
    end_date = datetime.strptime(end_time, '%Y-%m-%d') if end_time else None

    # 否则进行数据库查询
    query = {'period': period.value, 'adjust': adjust.value}
    if start_date:
        query.setdefault('date', {}).update({'$gte': start_date})
    if end_date:
        query.setdefault('date', {}).update({'$lte': end_date})

    result = list(collection.find(query, {'_id': False}).sort('date', -1))
    return result

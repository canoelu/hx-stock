from datetime import datetime
import os.path
import sys


# 加载其他模块
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from job.storeStocks.storeAllStockBaseInfo import store_all_stock_base_info
from job.storeStocks.storeTechCxsl import store_tech_cxsl_stocks,store_tech_cxfl_stocks
from job.storeStocks.storeTechLjqs import store_tech_ljqs_stocks
from job.storeStocks.storeTechcxd import store_tech_cxdg_stocks
from job.storeStocks.storeTechlxxd import store_tech_lxsz_stocks, store_tech_lxxd_stocks
from job.storeStocks.storeTechXzjp import store_tech_xzjp_stocks
from job.storeStocks.storeTechXstp import store_tech_xstp_stocks


def storeStockTech():
    # 获取股票列表
    store_all_stock_base_info()
    # 获取持续缩量、获取持续放量
    store_tech_cxsl_stocks()
    store_tech_cxfl_stocks()
    # 获取量价齐升
    store_tech_ljqs_stocks()
    
    # 持续新高新低
    store_tech_cxdg_stocks()
    # 连续上涨
    store_tech_lxsz_stocks()
    # 连续下跌
    store_tech_lxxd_stocks()
    # 险资举牌
    store_tech_xzjp_stocks()
    # 向上突破
    store_tech_xstp_stocks()
   
    

if __name__ == '__main__':
    storeStockTech()

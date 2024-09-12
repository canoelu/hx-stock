import schedule
import time
from datetime import datetime
import os.path
import sys
# 加载其他模块
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from job.storeStocks.storeAllStockBaseInfo import store_all_stock_base_info
from job.storeStocks.storeTechCxsl import store_tech_cxsl_stocks,store_tech_cxfl_stocks
from job.storeStocks.storeTechLjqs import store_tech_ljqd_stocks
from job.storeStocks.storeTechcxd import store_tech_cxdg_stocks

def job():
    # 获取股票列表
    store_all_stock_base_info()
    # 获取持续缩量、获取持续放量
    store_tech_cxsl_stocks()
    store_tech_cxfl_stocks()
    # 获取量价齐升
    store_tech_ljqd_stocks()
    # store_tech_cxdg_stocks
    store_tech_cxdg_stocks()
    

# 每个工作日的9:30执行任务
schedule.every().monday.at("09:15").do(job)
schedule.every().tuesday.at("09:15").do(job)
schedule.every().wednesday.at("09:15").do(job)
schedule.every().thursday.at("09:15").do(job)
schedule.every().friday.at("09:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

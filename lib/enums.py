# enums.py

from enum import Enum

class PeriodEnum(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'

class AdjustEnum(str, Enum):
    NOT_ADJUST = ''  # 不复权
    QFQ = 'qfq'      # 前复权
    HFQ = 'hfq'      # 后复权
class CxdEnum(str,Enum):
    CYXD= "monthLow" #创月新低
    BNXD= "halfLow" #半年新低
    YNXD="yearLow",#一年新低
    LSXD= "hisLow"#历史新低
class CxgEnum(str,Enum):
    CYXG= "monthHigh" #创月新高
    BNXG= "halfHigh" #半年新高
    YNXG= "yearHigh" #一年新高
    LSXG= "hisHigh" #历史新高
class XstpEnum(str,Enum):
    AVG5= "5avg" 
    AVG10= "10avg" 
    AVG20= "20avg" 
    AVG30= "30avg" 
    AVG60= "60avg" 
    AVG90= "90avg" 
    AVG250= "250avg" 
    AVG500= "500avg" 
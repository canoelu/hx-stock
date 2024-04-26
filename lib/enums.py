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

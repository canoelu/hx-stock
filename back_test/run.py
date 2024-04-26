from SmaCross import SmaCross
from BollStrategy import BollStrategy
from StrategyRunner import StrategyRunner
from TurtleStrategy import TurtleStrategy
from RSIStrategy import RSIStrategy
from datetime import datetime

# 示例用法
start_date = datetime(2023, 4, 3)  # 回测开始时间
end_date = datetime.now()  # 回测结束时间

stock_code='001311'
# stock_code='002466'
# 运行SMA交叉策略
# sma_runner = StrategyRunner(SmaCross, stock_code, start_date, end_date, pfast=5, pslow=20)
# sma_runner.backtest()

# # 运行Bollinger带策略
boll_runner = StrategyRunner(BollStrategy, stock_code, start_date, end_date, size=1800, period=20, devfactor=2)
boll_runner.backtest()

# 运行海龟策略
# turble_runner = StrategyRunner(TurtleStrategy, stock_code, start_date, end_date)
# turble_runner.backtest()
# RSI
# rsiStrategy = StrategyRunner(RSIStrategy, stock_code, start_date, end_date)
# rsiStrategy.backtest()

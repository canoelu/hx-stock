import backtrader as bt
import pandas as pd
from BaseStrategy import BaseStrategy

class TurtleStrategy(BaseStrategy,bt.Strategy):
    # 默认参数
    params = (
        ('long_period', 20),     # 长周期
        ('short_period', 10),    # 短周期
        # ('printlog', False),      # 是否打印日志
    )

    def __init__(self):
        super().__init__()

        # 初始化变量
        self.order = None
        self.buyprice = 0
        self.buy_size = 0
        self.buy_count = 0
        # 唐奇安通道和平均真实波幅指标
        self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.long_period)
        self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.short_period)
        self.ATR = bt.indicators.AverageTrueRange(period=14)
        # 价格与上下轨线的交叉
        self.buy_signal = bt.ind.CrossUp(self.data.close, self.H_line)
        self.sell_signal = bt.ind.CrossDown(self.data.close, self.L_line)

    def next(self):
        if self.order:
            return

        # 入场条件：价格突破上轨线且空仓时
        if self.buy_signal and self.buy_count == 0:
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR
            self.buy_size = int(self.buy_size / 100) * 100
            self.sizer.p.stake = self.buy_size
            self.buy_count = 1
            self.order = self.buy()

        # 加仓条件：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）
        elif self.data.close[0] > self.buyprice + 0.5 * self.ATR[0] and 0 < self.buy_count <= 4:
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR
            self.buy_size = int(self.buy_size / 100) * 100
            self.sizer.p.stake = self.buy_size
            self.order = self.buy()
            self.buy_count += 1

        # 离场条件：价格跌破下轨线且持仓时
        elif self.sell_signal and self.buy_count > 0:
            self.order = self.sell()
            self.buy_count = 0

        # 止损条件：价格跌破买入价的2个ATR且持仓时
        elif self.data.close[0] < (self.buyprice - 2 * self.ATR[0]) and self.buy_count > 0:
            self.order = self.sell()
            self.buy_count = 0
    
    
         
   

    

     
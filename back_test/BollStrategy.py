import backtrader as bt
import pandas as pd
from BaseStrategy import BaseStrategy

class BollStrategy(BaseStrategy,bt.Strategy):
    params = (('size', 1800), ('period', 20), ('devfactor', 2),)
    
    def __init__(self):
        super().__init__()
        self.name='SMA交叉策略'
        self.boll = bt.indicators.BollingerBands(self.datas[0], period=self.params.period, devfactor=self.params.devfactor)
    
    def next(self):
        if not self.position:
            if self.data.close <= self.boll.lines.bot:
                self.order = self.buy(size=self.params.size)
        else:
            if self.data.close >= self.boll.lines.top:
                self.order = self.sell(size=self.params.size)
  
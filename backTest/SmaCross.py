import backtrader as bt
import pandas as pd
from BaseStrategy import BaseStrategy



class SmaCross(BaseStrategy,bt.Strategy):
    params = (('pfast', 5), ('pslow', 20),('printlog', False),)
    
    def __init__(self):
        super().__init__()
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        self.name='Sma带策略'
        
    
    def next(self):
        if self.crossover > 0:
            self.close()
            self.buy(size=1500)
        elif self.crossover < 0:
            self.close()
            self.sell(size=1500)
   
        
    
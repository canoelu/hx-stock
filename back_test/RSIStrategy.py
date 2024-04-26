import backtrader as bt
import pandas as pd
from BaseStrategy import BaseStrategy

# 这个目前只是简单的示例，无法应用
class RSIStrategy(BaseStrategy,bt.Strategy):
    params=(('short',30),
            ('long',70),)
    
    def __init__(self):
        super().__init__()
        self.rsi = bt.indicators.RSI_SMA(
                   self.data.close, period=21)
         
        self.name='rsi带策略'
        
    
    def next(self):
        if not self.position:
            if self.rsi < self.params.short:
                self.buy()
        else:
            if self.rsi > self.params.long:
                self.sell()
 
import backtrader as bt
import pandas as pd
import csv

class BaseStrategy(bt.Strategy):
    """
    基础策略类，继承自Backtrader的策略类。

    参数：
        printlog (bool): 是否打印日志，默认为True。

    成员变量：
        trade_records (pd.DataFrame): 交易记录的DataFrame。

    方法：
        start(): 策略启动时调用的方法。
        prenext(): 策略未成熟时调用的方法。
        next(): 策略每个交易日调用的方法。
        stop(): 策略停止时调用的方法。
        log(txt, dt=None, doprint=False): 记录日志的方法。
        notify_order(order): 通知订单执行情况的方法。
        notify_trade(trade): 通知交易情况的方法。
    """
    
    params = (('printlog', True),)

    def __init__(self):
        """
        初始化方法，在策略启动时调用。
        """
        self.trade_records = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'Cost', 'Commission'])

    def start(self):
        """
        策略启动时调用的方法。
        """
        self.mystats = csv.writer(open("./mystats.csv", "w"))
        self.mystats.writerow(['datetime',
                               'drawdown', 'maxdrawdown', 
                               'timereturn',
                               'value', 'cash'])
        self.log("Strategy started.")

    def prenext(self):
        """
        策略未成熟时调用的方法。
        """
        self.log("Strategy not mature yet.")

    def next(self): 
        """
        策略每个交易日调用的方法。
        """
        self.mystats.writerow([self.data.datetime.date(-1).strftime('%Y-%m-%d'),
                               '%.4f' % self.stats.drawdown.drawdown[0],
                               '%.4f' % self.stats.drawdown.maxdrawdown[0],
                               '%.4f' % self.stats.timereturn.line[0],
                               '%.4f' % self.stats.broker.value[0],
                               '%.4f' % self.stats.broker.cash[0]]) 

    def stop(self):  
        """
        策略停止时调用的方法。
        """
        self.mystats.writerow([self.data.datetime.date(0).strftime('%Y-%m-%d'),
                               '%.4f' % self.stats.drawdown.drawdown[0],
                               '%.4f' % self.stats.drawdown.maxdrawdown[0],
                               '%.4f' % self.stats.broker.value[0],
                               '%.4f' % self.stats.broker.cash[0]])
        self.log("Strategy stopped.")

    def log(self, txt, dt=None, doprint=False):
        """
        记录日志的方法。

        参数：
            txt (str): 要记录的文本。
            dt (datetime, optional): 要记录的日期时间，默认为None。
            doprint (bool, optional): 是否打印日志，默认为False。
        """
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def notify_order(self, order):
        """
        通知订单执行情况的方法。

        参数：
            order (bt.Order): 订单对象。
        """
        if order.status in [order.Completed]:
            action = '买入' if order.isbuy() else '卖出'
            # 将交易记录添加到DataFrame中
            new_record = pd.DataFrame({
                'Datetime': [self.datas[0].datetime.datetime()],
                'Action': [action],
                'Price': [order.executed.price],
                'Cost': [order.executed.value],
                'Commission': [order.executed.comm]
            })
            self.trade_records = pd.concat([self.trade_records, new_record], ignore_index=True)

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None
        self.log(self.trade_records)

    def notify_trade(self, trade):
        """
        通知交易情况的方法。

        参数：
            trade (bt.Trade): 交易对象。
        """
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

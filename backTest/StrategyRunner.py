import pandas as pd
import backtrader as bt
from datetime import datetime
import akshare as ak
from TradeSizer import TradeSizer
from OrderObserver import my_Trades,my_BuySell
import matplotlib.pyplot as plt
import pyfolio as pf
import matplotlib.ticker as ticker # 导入设置坐标轴的模块


plt.style.use('dark_background')

# plt.style.use('seaborn') # 使用 seaborn 主题
plt.rcParams['figure.figsize'] = 20, 10  # 全局修改图大小
class StrategyRunner:
    def __init__(self, strategy_class, stock_symbol, start_date, end_date, **kwargs):
        self.strategy_class = strategy_class
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.kwargs = kwargs
    
    def backtest(self):
        # 获取股票数据
        stock_hfq_df = ak.stock_zh_a_hist(symbol=self.stock_symbol, adjust="qfq").iloc[:, :6]
        stock_hfq_df.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])

        # 加载数据
        data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=self.start_date, todate=self.end_date)

        # 初始化cerebro回测系统设置 
        cerebro = bt.Cerebro(stdstats=False)
        cerebro.addobserver(bt.observers.DrawDown)
        cerebro.addobserver(bt.observers.TimeReturn)
        cerebro.addobserver(bt.observers.Broker)
        cerebro.addobserver(my_Trades)
        cerebro.addobserver(my_BuySell)
        cerebro.adddata(data)
        cerebro.addstrategy(self.strategy_class, **self.kwargs)

        # 设置初始资本
        startcash = 100000
        cerebro.broker.setcash(startcash)
        # cerebro.addsizer(TradeSizer)    

        # 设置交易手续费
        cerebro.broker.setcommission(commission=0.001)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW') 
        cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
        
        # 运行回测系统
        results=cerebro.run()

        # 获取回测结束后的总资金
        portvalue = cerebro.broker.getvalue()
        pnl = portvalue - startcash
        # 计算最大回撤
        strat = results[0]
         

        print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
        max_drawdown = strat.analyzers.DW.get_analysis()
        print('回撤指标:',max_drawdown )
        # 打印结果
        print(f'策略: {self.strategy_class.__name__}')
        print(f'股票: {self.stock_symbol}')
        print(f'净收益: {round(pnl, 2)}')
        print(f'总资金: {round(portvalue, 2)}')
        
        
        # 提取收益序列
        pnl = pd.Series(strat.analyzers._TimeReturn.get_analysis())
        # 计算累计收益
        cumulative = (pnl + 1).cumprod()
        # 计算回撤序列
        max_return = cumulative.cummax()
        drawdown = (cumulative - max_return) / max_return
        # 计算收益评价指标
        # 按年统计收益指标
        perf_stats_year = (pnl).groupby(pnl.index.to_period('y')).apply(lambda data: pf.timeseries.perf_stats(data)).unstack()
        # 统计所有时间段的收益指标
        perf_stats_all = pf.timeseries.perf_stats((pnl)).to_frame(name='all')
        perf_stats = pd.concat([perf_stats_year, perf_stats_all.T], axis=0)
        perf_stats_ = round(perf_stats,4).reset_index()
        fig, (ax0, ax1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[1.5, 4]}, figsize=(20,8))
        cols_names = ['date', 'year\nshouyilv', 'total\nshouyilv', 'year\nbodonglv',
            'xiapu\nrate', 'kaerma\nrate', 'wendingxing', 'max\nhuice',
            'oumiga\nrate', 'suotinuo\nrate', 'piandu', 'fengdu', 'weibu\nrate',
            'meirifengxian\njiazhi']
        # 绘制表格
        ax0.set_axis_off() # 除去坐标轴
        table = ax0.table(cellText = perf_stats_.values, 
                        bbox=(0,0,1,1), # 设置表格位置， (x0, y0, width, height)
                        rowLoc = 'right', # 行标题居中
                        cellLoc='right' ,
                        colLabels = cols_names, # 设置列标题
                        colLoc = 'right', # 列标题居中
                        edges = 'open' # 不显示表格边框
                        )
        table.set_fontsize(13)

        # 绘制累计收益曲线
        ax2 = ax1.twinx()
        ax1.yaxis.set_ticks_position('right') # 将回撤曲线的 y 轴移至右侧
        ax2.yaxis.set_ticks_position('left') # 将累计收益曲线的 y 轴移至左侧
        # 绘制回撤曲线
        drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
        # 绘制累计收益曲线
        (cumulative).plot(ax=ax2, color='#F1C40F' , lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
        # 不然 x 轴留有空白
        ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
        # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(100)) 
        # 同时绘制双轴的图例
        h1,l1 = ax1.get_legend_handles_labels()
        h2,l2 = ax2.get_legend_handles_labels()
        plt.legend(h1+h2,l1+l2, fontsize=12, loc='upper left', ncol=1)

        fig.tight_layout() # 规整排版
        plt.show()
        tableau10 = [
            'blue', # 'steelblue', # 0
            'darkorange', # 1
            'green', # 2
            'crimson', # 3
            'mediumpurple', # 4
            'saddlebrown', # 5
            'orchid', # 6
            'gray', # 7
            'olive', # 8
            'mediumturquoise', # 9
        ]
        #策略运行完后，绘制图形
        colors = ['#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a8786e', '#ed97ca', '#a2a2a2', '#cdcc5d', '#6dccda']
        
        # 最后可视化
        cerebro.plot(
            iplot=False, 
            style='candel', # 设置主图行情数据的样式为蜡烛图,line
            lcolors=colors,
            plotdist=0.1,
            barup = '#ff0000', bardown='#98df8a', # 设置蜡烛图上涨和下跌的颜色
            volup='#ff0000', voldown='#98df8a', # 设置成交量在行情上涨和下跌情况下的颜色
            grid=False
        )

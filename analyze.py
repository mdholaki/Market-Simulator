import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, math
import csv
def plot_portfolio(fund, benchmark):
    
    #Read the value from the funds 
    ldt_timestamps = []
    ls_values = []
    fund_csv = csv.reader(open(fund, 'rU'), delimiter=',')    
    for row in fund_csv:
        ls_values.append(float(row[3]))
        ldt_timestamps.append(dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16))
    ts_fund = pd.TimeSeries(ls_values, index = ldt_timestamps)
    #print ts_fund
        
    #Retrieve Data for Benchmark 
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(ldt_timestamps[0], ldt_timestamps[-1], dt_timeofday)
    
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    bench_data = c_dataobj.get_data(ldt_timestamps, [benchmark], ls_keys)
    
    d_data = dict(zip(ls_keys, bench_data))
    benchmark_price = d_data['close'].values    
    mul = ts_fund[0] / benchmark_price[0]
    benchmark_price = mul * benchmark_price

    #Evaluate portfolio performance
    
    #Total risk of the portfolio
    daily_ret = tsu.daily(ts_fund.values)
    vol = daily_ret.std()
    
    #Average Daily Returns of the Portfolio
    avg_daily_ret = daily_ret.mean()
    
    #Calcluate sharpe ratio of the Portfolio (k = 252)
    sharpe_ratio = (avg_daily_ret/(vol)) * math.sqrt(252)    
    
    #Calculate the Cumulative Return of the portfolio
    cum_ret = ts_fund[-1]/ts_fund[0]
    
    #Evaluate portfolio performance
        
    #Total risk of the benchmark
    daily_ret_bench = tsu.daily(benchmark_price)
    vol_bench = daily_ret_bench.std()
    
    #Average Daily Returns of the Benchmark
    avg_daily_ret_bench = daily_ret_bench.mean()
    
    #Calcluate sharpe ratio of the benchmark (k = 252)
    sharpe_ratio_bench = (avg_daily_ret_bench/(vol_bench)) * math.sqrt(252)    
    
    #Calculate the Cumulative Return of the portfolio
    cum_ret_bench = benchmark_price[-1]/benchmark_price[0]    
    
    
    #Plot the performance of the fund and the benchmark 
    plt.clf()
    plt.plot(ldt_timestamps, ts_fund.values, ldt_timestamps, benchmark_price)
    plt.legend(['Portfolio', benchmark])
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.savefig('fund_performance.pdf', format='pdf')    
    plt.xticks(size='xx-small')
    plt.yticks(size='xx-small')    
    
    
    
    
    
    print '\nPortfolio Performance'
    print '---------------------------------------'
    print ldt_timestamps[0].strftime('Start Date: %B %d, %Y')
    print ldt_timestamps[-1].strftime('End Date: %B %d, %Y')
    print
    print 'Sharpe Ratio of the Fund: ' + str(sharpe_ratio)
    print 'Sharpe Ratio of ' + benchmark + ': ' + str(sharpe_ratio_bench) + '\n'
    print 'Total Return of the Fund: ' + str(cum_ret)
    print 'Total Return of ' + benchmark + ': ' + str(cum_ret_bench[0]) + '\n'
    print 'Standard Deviation of the Fund: ' + str(vol)
    print 'Standard Deviate of ' + benchmark + ': ' + str(vol_bench) + '\n'
    print 'Average Daily Return of the Fund: ' + str(avg_daily_ret)
    print 'Average Daily Return of ' + benchmark + ': ' + str(avg_daily_ret_bench) + '\n'
    
    
    
    
    
    
    

if __name__ == '__main__':
    fund = 'values.csv'
    benchmark = '$SPX'
    
    plot_portfolio(fund, benchmark)
    
    
    
    

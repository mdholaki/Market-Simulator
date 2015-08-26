import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
from itertools import combinations_with_replacement

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, math
import copy
import QSTK.qstkstudy.EventProfiler as ep

def find_events(symbols, d_data):
    df_close = d_data['close']
    ts_market = df_close['SPY']
    
    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN
    
    # Time stamps for the event range
    ldt_timestamps = df_close.index    
    
    for sym in symbols:
            for i in range(1, len(ldt_timestamps)): 
                symprice_today = df_close[sym].ix[ldt_timestamps[i]]
                symprice_yest = df_close[sym].ix[ldt_timestamps[i - 1]]
                
                if symprice_today < 5 and symprice_yest > 5:
                    df_events[sym].ix[ldt_timestamps[i]] = 1                    
    return df_events

if __name__ == '__main__':
    #Set Date Parameters and load in the data
    start_year = 2008
    start_month = 1
    start_day = 1
    
    #Enter the end date
    
    end_year = 2009
    end_month = 12
    end_day = 31
    
    #Create datetime structures for start and end 
    startdate = dt.datetime(start_year, start_month, start_day)
    enddate = dt.datetime(end_year, end_month, end_day)  
    
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    
    
    #Get all S&P500 stock symbols 
    dataobj = da.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list("sp5002008")
    symbols.append('SPY')
    
    #Retrieve data from Yahoo
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)    
            
    df_events = find_events(symbols, d_data)
    
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')    
    
    

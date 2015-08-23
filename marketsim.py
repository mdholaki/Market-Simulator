import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da


import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, math
import copy
import QSTK.qstkstudy.EventProfiler as ep
import csv
from pylab import *

def simulator(starting_val, orders, values):
    
    #Read the dates and Symbols
    ldt_timestamps_trade = list()
    ls_symbols = list()
    
    #Read in all dates and symbols into 2 lists from the CSV file 
    orders_csv = csv.reader(open(orders, 'rU'), delimiter=',')    
    for row in orders_csv:        
        ls_symbols.append(row[3])
        ldt_timestamps_trade.append(dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16))    
            
    
    #Remove duplicate symnols from the list     
    ls_symbols = list(set(ls_symbols))    
    ldt_timestamps_trade = list(set(ldt_timestamps_trade))
    ldt_timestamps_trade = sorted(ldt_timestamps_trade)
    
    #Retrieve Stock data 
    
    #Set NYSE dates 
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(ldt_timestamps_trade[0], ldt_timestamps_trade[-1], dt_timeofday)
    
    
    #Load the data 
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    df_close = d_data['close']
    df_close = df_close.fillna(method='ffill')
    df_close = df_close.fillna(method='bfill')    
        
    #Create the trade matrix
    df_vals = pd.DataFrame(index=ldt_timestamps, columns=ls_symbols)
    df_vals = df_vals.fillna(0.0)    

    orders_csv = csv.reader(open(orders, 'rU'), delimiter=',')    
    for row in orders_csv:
        if row[4] == "Buy":
            num_shares = float(row[5])
        else:
            num_shares = float(0 - float(row[5]))
        df_vals[row[3]].ix[dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16)] = num_shares        
    
    #Initialize am empty timeseries to track cash
    ts_cash = pd.TimeSeries(0.0, index=ldt_timestamps)
    
    #Fill the timeseries with appropiate data
    ts_cash[0] = starting_val
    
    
    for day in ldt_timestamps:
        for sym in ls_symbols:
            price = d_data['close'].ix[day]
            trade = df_vals[sym].ix[day]            
            ts_cash[day] += ((float(trade)* -1) * float(price[sym]))    
     
    #Add cash attribute to the price data 
    df_close = d_data['close']
    df_close['_Cash'] = 1.0
                
    #Add cash time series into the trade matrix 
    df_vals['_Cash'] = ts_cash   
    
    #Convert the trade matrix into a holding matrix
    
    for sym in ls_symbols:
        df_vals[sym] = df_vals[sym].cumsum()
    
    df_vals['_Cash'] = df_vals['_Cash'].cumsum()
    
    #Portfolio value
    ts_port = pd.TimeSeries(0.0, index=ldt_timestamps)
    
    
    for day in ldt_timestamps:
        share_val_total = 0
        for sym in ls_symbols:
            price = d_data['close'].ix[day]
            trade = df_vals[sym].ix[day]            
            share_val_curr = ((float(trade)) * float(price[sym]))
            share_val_total += share_val_curr
        portfolio_val = share_val_total + df_vals['_Cash'].ix[day]
        ts_port[day] = portfolio_val
    
    #Write data to CSV
    writer = csv.writer(open(values, 'wb'), delimiter=',')
    for row in ts_port.index:
        data_entry = [str(row.year), str(row.month),str(row.day), str(ts_port[row])]
        writer.writerow(data_entry)
    
    
if __name__ == '__main__':
    
    #starting value for the portfolio 
    starting_val = 1000000
    #The file where the orders are located 
    orders = 'Order_Files\orders.csv'
    #Output file -- will contain value of the portfolio everyday 
    values = 'values.csv'
    
    simulator(starting_val, orders, values)
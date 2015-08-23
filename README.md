# Market-Simulator
Market simulation tool which uses real world market data to test investment strategies and analyze portfolios. 

Given a portfolio's starting cash value and a csv which contains the portfolios investment strategy, the marketsim.py will output
values.csv which tracks the portfolio's performance over a period of time using historical market data. 

A second file (analyze.py) is used to analyze the portfolio's performance. The program calculates the portfolio's sharpe ratio, average
daily return, risk, and the portfolio's cumulative return. It also compares the performance of the portfolio against a benchmark
(e.g. S&p 500). 


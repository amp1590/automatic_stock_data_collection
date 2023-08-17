#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import shutil
import time
import datetime
import csv
import os

# Collecting list of tickers for S&P500 index
sp500url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
data_table=pd.read_html(sp500url)
ticker_list = data_table[0]['Symbol'].tolist() #There are 2 tables, we want the first table


# Cleaning the list of tickers
for i in range(len(ticker_list)):
    if ticker_list[i] == 'BRK.B':
        ticker_list[i]='BRK-B'
    elif ticker_list[i] == 'BF.B':
        ticker_list[i]='BF-B'        
print("Total no. of companies in the list: ",len(ticker_list))


# Setting the interval and date range of the desired dataset
interval = '1wk'
start_date = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
end_date = int(time.mktime(datetime.datetime(2021, 6, 29, 23, 59).timetuple()))


# Creating a dedicated directory to save the dataset
directory = "data_sp500stocks"
parent_dir = "/Users/aruni/Documents"
final_path = os.path.join(parent_dir, directory)
if os.path.exists(final_path):
    shutil.rmtree(final_path)
os.mkdir(final_path)


# Collecting historical data of all the comapnies 
ignored_stocks=0
for ticker in ticker_list:
    try:
        df = yf.download(tickers=ticker,start=start_date,end=end_date, interval=interval, rounding=True)
        df.reset_index(inplace=True)
        df = df.rename(columns = {'index':'Date'})
        df["Name"]=ticker
        df=df.drop(columns=['Adj Close'])
        
        # Save the modified DataFrame to a new CSV file
        df.to_csv(final_path+"/"+ticker+".csv", index=False)
    except Exception:
        ignored_stocks=ignored_stocks+1
        print("The company ",ticker," didn't exist in this entire time period")
        None
print("Total no. of companies whose data has been collected: ", len(tickers)-ignored_stocks)


# In[ ]:





# In[ ]:





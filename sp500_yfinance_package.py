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
interval = '1d'
start_date = '2022-01-01'
end_date = '2022-12-31'

"""
# Creating a dedicated directory to save the dataset
directory = "data_sp500stocks"
absolute_path = "/Users/aruni/Documents"
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)

"""
# Creating a dedicated directory to save the dataset
directory = "data_sp500stocks"
absolute_path = os.path.dirname(__file__)
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)


# Collecting historical data of all the companies 
ignored_stocks=0
for ticker in ticker_list:
    # Downloading data for a stock
    df = yf.download(tickers=ticker,start=start_date,end=end_date, interval=interval, auto_adjust=True, rounding=True, progress=False)
    if len(df)==0:
        ignored_stocks=ignored_stocks+1
        print("The company ",ticker," didn't exist in this entire time period")
        continue
    # Converting "Date" index of the DataFrame into a column
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'Date'})
    #Adding "Name" column
    df["Name"]=ticker
    # Save the modified DataFrame to a new CSV file
    df.to_csv(relative_path+"/"+ticker+".csv", index=False)
print("Total no. of companies whose data has been collected: ", len(ticker_list)-ignored_stocks)


# In[ ]:





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
import requests
import io

# Collecting list of tickers for Nasdaq index 
'''
#For Nasdaq-100 from wiki
nasdaq100url='https://en.wikipedia.org/wiki/Nasdaq-100'
data_table=pd.read_html(nasdaq100url)
ticker_list = data_table[4]['Ticker'].tolist() #There are more than 5 tables, we want the 5th table
'''
## For Nasdaq all companies from datahub.io
nasdaq_url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(nasdaq_url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
ticker_list = companies['Symbol'].tolist()

print("Total no. of companies in the list: ", len(ticker_list))


# Setting the interval and date range of the desired dataset
interval = '1d'
start_date = '2022-01-01'
end_date = '2022-12-31'


# Creating a dedicated directory to save the dataset
directory = "data_nasdaq_stocks"
absolute_path = "/Users/aruni/Documents"
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)

"""
# Creating a dedicated directory to save the dataset
directory = "data_nasdaq_stocks"
absolute_path = os.path.dirname(__file__)
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)
"""

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





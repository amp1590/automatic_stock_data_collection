#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import shutil
import time
import datetime
import csv
import os
import requests
import io

##Collecting list of tickers for Nasdaq index 
'''
#For Nasdaq-100 from wiki
nasdaq100url='https://en.wikipedia.org/wiki/Nasdaq-100'
data_table=pd.read_html(nasdaq100url)
tickers = data_table[4]['Ticker'].tolist() #There are more than 5 tables, we want the 5th table
'''
#For Nasdaq all companies from datahub.io
nasdaq_url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(nasdaq_url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
ticker_list = companies['Symbol'].tolist()

print("Total no. of companies in the list: ", len(tickers))


##Setting the interval and date range of the desired dataset
interval = '1d'
start_date = int(time.mktime(datetime.datetime(2022, 1, 1, 23, 59).timetuple()))
end_date = int(time.mktime(datetime.datetime(2022, 12, 31, 23, 59).timetuple()))

"""
# Creating a dedicated directory to save the dataset
directory = "data_nasdaq_stocks_2"
absolute_path = "/Users/aruni/Documents"
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)

"""
# Creating a dedicated directory to save the dataset
directory = "data_nasdaq_stocks_2"
absolute_path = os.path.dirname(__file__)
relative_path = os.path.join(absolute_path, directory)
if os.path.exists(relative_path):
    shutil.rmtree(relative_path)
os.mkdir(relative_path)



# Collecting historical data of all the comapnies 
ignored_stocks=0
for ticker in ticker_list:
    try:
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        # Considering only the Adjusted Close column as Close column
        df=df.drop(columns=['Close'])
        df.rename(columns = {'Adj Close':'Close'}, inplace = True)
        #Adding "Name" column
        df["Name"]=ticker
        
        # Iterate through each column (excluding the date column) and round to two decimal places
        for column in df.columns:
            if column != 'Date' and column!='Name' and df[column].dtype == 'float64':
                df[column] = df[column].round(2)
        
        # Save the modified DataFrame to a new CSV file
        df.to_csv(relative_path+"/"+ticker+".csv", index=False)
    except Exception:
        ignored_stocks=ignored_stocks+1
        print("The company ",ticker," didn't exist in this entire time period")
        None
print("Total no. of companies whose data has been collected: ", len(ticker_list)-ignored_stocks)
    


# In[ ]:





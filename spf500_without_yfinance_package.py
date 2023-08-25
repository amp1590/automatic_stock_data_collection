#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import shutil
import time
import datetime
import csv
import os

#Collecting list of tickers for S&P500 index
sp500url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
data_table=pd.read_html(sp500url)
ticker_list = data_table[0]['Symbol'].tolist() #There are 2 tables, we want the first table


#Cleaning the list of tickers
for i in range(len(ticker_list)):
    if ticker_list[i] == 'BRK.B':
        ticker_list[i]='BRK-B'
    elif ticker_list[i] == 'BF.B':
        ticker_list[i]='BF-B'        
print("Total no. of companies in the list: ",len(ticker_list))


#Setting the interval and date range of the desired dataset
interval = '1d'
start_date = int(time.mktime(datetime.datetime(2022, 1, 1, 23, 59).timetuple()))
end_date = int(time.mktime(datetime.datetime(2022, 12, 31, 23, 59).timetuple()))

"""
# Creating a dedicated directory to save the dataset
directory = "data_sp500stocks_2"
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



#Collecting historical data of all the comapnies 
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





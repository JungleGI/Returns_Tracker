# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:45:22 2023

@author: Ulrich
"""

import requests
import json
import pandas as pd
import streamlit as st
import datetime
import time

st.title('Performance Tracker')

#Time input
user_date = st.date_input('Start Date', value="today")
start_time = round((time.mktime(user_date.timetuple())))*1000
end_time = round(time.mktime(datetime.datetime.now().timetuple()))*1000

#Tickers
tickers = ('bitcoin','ethereum','solana','avalanche','polygon','injective-protocol','render-token','aave','the-sandbox','gala','fetch','enjin-coin','singularitynet','xrp','chainlink')


#Data
def getdata(symbol,start,end):
    url = f"https://api.coincap.io/v2/assets/{symbol}/history?interval=m30&start={start_time}&end={end_time}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text.encode('utf8'))
    price_data = json_data["data"]
    df = pd.DataFrame(price_data)
    return(df)

df = pd.DataFrame()
for ticker in tickers:
    df_tmp = getdata(ticker,start_time,end_time)
    df_tmp['Ticker'] = ticker
    df = pd.concat([df,df_tmp])

#Formatting Data
df['date'] = pd.to_datetime(df.date).dt.tz_localize(None)
df['Time'] = df['date'].dt.strftime('%m-%d %H:%M')
df.set_index('Time', inplace=True)
df = df[['priceUsd','Ticker']]
df.columns = ['price','ticker']
df1 = df.pivot_table(index=['Time'],columns='ticker', values=['price'])
df1.columns = [col[1] for col in df1.columns.values]

#Calcs
df_daily_returns = df1.pct_change()
df_daily_returns = df_daily_returns[1:]
df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1

#Charting
Chart1 = df_cum_daily_returns[['bitcoin','solana','ethereum','avalanche','polygon','injective-protocol','aave']]
Chart2 = df_cum_daily_returns[['bitcoin','ethereum','render-token','fetch','singularitynet','xrp','chainlink']]
Chart3 = df_cum_daily_returns[['bitcoin','ethereum','the-sandbox','gala','enjin-coin']]
st.line_chart(Chart1)
st.line_chart(Chart2)
st.line_chart(Chart3)





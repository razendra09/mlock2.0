from smartapi import SmartConnect
import pandas as pd
from datetime import datetime, timedelta
import credentials
import requests
import numpy as np
from time import time, sleep
from talib.abstract import *
import threading
import warnings
warnings.filterwarnings('ignore')

# Collect Historical Data
def getHistoricalAPI(token, interval='THREE_MINUTE'):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=20)
    from_date_format = from_date.strftime("%Y-%m-%d %H:%M")
    to_date_format = to_date.strftime("%Y-%m-%d %H:%M")
    try:
        historicParam = {
            "exchange": "NSE",
            "symboltoken": token,
            "interval": interval,
            "fromdate": from_date_format,
            "todate": to_date_format
        }
        candel_json = credentials.SMART_API_OBJ.getCandleData(historicParam)
        return calculate_inidcator(candel_json)
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))

# Filter Data & Create Data Frame & Apply Indicator
def calculate_inidcator(res_json):
    columns = ['timestamp', 'O', 'H', 'L', 'C', 'V']
    df = pd.DataFrame(res_json['data'], columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S')
    df['EMA'] = EMA(df.C, timeperiod=26)
    df['RSI'] = RSI(df.C, timeperiod=14)
    df['ATR'] = ATR(df.H, df.L, df.C, timeperiod=20)
    df['CROSS_UP'] = df['CROSS_DOWN'] = df['RSI_UP'] = 0
    df = df.round(decimals=2)

    for i in range(20, len(df)):
        if df['C'][i - 1] <= df['EMA'][i - 1] and df['C'][i] > df['EMA'][i]:
            df['CROSS_UP'][i] = 1
        if df['C'][i - 1] >= df['EMA'][i - 1] and df['C'][i] < df['EMA'][i]:
            df['CROSS_DOWN'][i] = 1
        if df['RSI'][i] > 30:
            df['RSI_UP'][i] = 1

    print(df.tail(10))
    return df

# Generate Signal
def checkSingnal():
    start = time()
    global TRADED_SYMBOL

    for symbol in SYMBOL_LIST:
        if symbol not in TRADED_SYMBOL:
            tokenInfo = getTokenInfo(symbol).iloc[0]
            token = tokenInfo['token']
            symbol = tokenInfo['symbol']
            print(symbol, token)
            candel_df = getHistoricalAPI(token)
            if candel_df is not None:
                latest_candel = candel_df.iloc[-1]
                if latest_candel['CROSS_UP'] == 1 and latest_candel['RSI_UP'] == 1:
                    ltp = latest_candel['C']
                    SL = ltp - 2 * latest_candel['ATR']
                    target = ltp + 5 * latest_candel['ATR']
                    qty = 1  # qunatity to trade

                    res1 = place_order(token, symbol, qty, 'BUY', 'MARKET', 0)  # buy order
                    # res2 = place_order(token,symbol,qty,'SELL','STOPLOSS_MARKET',0,variety='STOPLOSS',triggerprice= SL) #SL order
                    # res3 = place_order(token,symbol,qty,'SELL','LIMIT') #taget order ,target
                    print(res1)

                    #
                    # print(f'Order Placed for {symbol} SL {SL}  TGT {target} QTY {qty} at {datetime.now()}')
                    # TRADED_SYMBOL.append(symbol)

    interval = timeFrame - (time() - start)
    print(interval)
    threading.Timer(interval, checkSingnal).start()

# Create Orders
def place_order(token,symbol,qty,buy_sell,ordertype,price,variety='NORMAL',exch_seg='NSE',triggerprice=0):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "DELIVERY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty,
            "triggerprice":triggerprice
            }
        orderId=credentials.SMART_API_OBJ.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))
# Results with Telegram Notifications









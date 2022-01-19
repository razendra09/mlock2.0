from smartapi import SmartConnect
import json
import pandas as pd
from datetime import datetime, timedelta
#from talib.abstract import *

# Account Authentication
apikey='9QxhQKPE'
username='R603324'
pwd='Af7338@@'

obj=SmartConnect(api_key=apikey)
data = obj.generateSession(username, pwd)
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()

# Get Historical Data of any Instrument

def historicaldata():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=20)
    from_date_format = from_date.strftime("%Y-%m-%d %H:%M")
    to_date_format = to_date.strftime("%Y-%m-%d %H:%M")
    stock_token= 14368
    stock_exchange= "NSE"
    data_interval= "FIVE_MINUTE"
    try:
        historicParam = {
            "exchange": stock_exchange,
            "symboltoken": stock_token,
            "interval": data_interval,
            "fromdate": from_date_format,
            "todate": to_date_format,
        }

        return obj.getCandleData(historicParam)
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))

# Create Data frame & filter data

res_json = historicaldata()
columns = ['timestamp','OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
df = pd.DataFrame(res_json['data'], columns=columns)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S')
#df['RSI'] = RSI(df.C, timeperiod=14)


#Testing Indicator Calculating Heikin Ashi Close Price

HAdf = df[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]
HAdf['CLOSE'] = round(((df['OPEN'] + df['HIGH'] + df['LOW'] + df['CLOSE'])/4),2)

# print(HAdf['CLOSE'])

# Calculating Heikin Ashi Open Price
for i in range(len(df)):
    if i == 0:
        HAdf.iat[0,0] = round(((df['OPEN'].iloc[0] + df['CLOSE'].iloc[0])/2),2)
    else:
        HAdf.iat[i,0] = round(((HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2),2)


#print(HAdf['OPEN'])

# Calculating Heikin Ashi High & Low Price

HAdf['HIGH'] = HAdf.loc[:,['OPEN', 'CLOSE']].join(df['HIGH']).max(axis=1)
HAdf['LOW'] = HAdf.loc[:,['OPEN', 'CLOSE']].join(df['LOW']).min(axis=1)

print(HAdf.tail(100))

#  Data Chart

# import plotly.graph_objects as go
#
# fig1 = go.Figure(data=[go.Candlestick(x=df.index,
#                 open=df.OPEN,
#                 high=df.HIGH,
#                 low=df.LOW,
#                 close=df.CLOSE)])
#
# fig1.update_layout(yaxis_range = [1500,2500],
#            title = 'Candlestick Chart: Idea',
#            xaxis_title = 'Date',
#            yaxis_title = 'Price')
# fig1.show()
#
# fig2 = go.Figure(data=[go.Candlestick(x=HAdf.index,
#                 open=HAdf.OPEN,
#                 high=HAdf.HIGH,
#                 low=HAdf.LOW,
#                 close=HAdf.CLOSE)] )
#
#
# fig2.update_layout(yaxis_range = [1500,2500],
#           title = 'Heikin Ashi Chart: RELIANCE',
#           xaxis_title = 'Date',
#           yaxis_title = 'Price')
# fig2.show()







# # Apply Indicator to data
#
# def calculate_inidcator(res_json):
#     columns = ['timestamp', 'O', 'H', 'L', 'C', 'V']
#     df = pd.DataFrame(res_json['data'], columns=columns)
#     df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S')
#     df['EMA'] = EMA(df.C, timeperiod=26)
#     df['RSI'] = RSI(df.C, timeperiod=14)
#     df['ATR'] = ATR(df.H, df.L, df.C, timeperiod=20)
#     df['CROSS_UP'] = df['CROSS_DOWN'] = df['RSI_UP'] = 0
#     df = df.round(decimals=2)
#
#     for i in range(20, len(df)):
#         if df['C'][i - 1] <= df['EMA'][i - 1] and df['C'][i] > df['EMA'][i]:
#             df['CROSS_UP'][i] = 1
#         if df['C'][i - 1] >= df['EMA'][i - 1] and df['C'][i] < df['EMA'][i]:
#             df['CROSS_DOWN'][i] = 1
#         if df['RSI'][i] > 30:
#             df['RSI_UP'][i] = 1
#
#     print(df.tail(10))
#     return df
#
# # Check Signal
# def checkSingnal():
#     start = time()
#     global TRADED_SYMBOL
#
#     for symbol in SYMBOL_LIST:
#         if symbol not in TRADED_SYMBOL:
#             tokenInfo = getTokenInfo(symbol).iloc[0]
#             token = tokenInfo['token']
#             symbol = tokenInfo['symbol']
#             print(symbol, token)
#             candel_df = getHistoricalAPI(token)
#             if candel_df is not None:
#                 latest_candel = candel_df.iloc[-1]
#                 if latest_candel['CROSS_UP'] == 1 and latest_candel['RSI_UP'] == 1:
#                     ltp = latest_candel['C']
#                     SL = ltp - 2 * latest_candel['ATR']
#                     target = ltp + 5 * latest_candel['ATR']
#                     qty = 1  # qunatity to trade
#
#                     res1 = place_order(token, symbol, qty, 'BUY', 'MARKET', 0)  # buy order
#                     # res2 = place_order(token,symbol,qty,'SELL','STOPLOSS_MARKET',0,variety='STOPLOSS',triggerprice= SL) #SL order
#                     # res3 = place_order(token,symbol,qty,'SELL','LIMIT') #taget order ,target
#                     print(res1)
#
#                     #
#                     # print(f'Order Placed for {symbol} SL {SL}  TGT {target} QTY {qty} at {datetime.now()}')
#                     # TRADED_SYMBOL.append(symbol)
#
#     interval = timeFrame - (time() - start)
#     print(interval)
#     threading.Timer(interval, checkSingnal).start()
#
# # Order Management
#
# def place_order(token,symbol,qty,buy_sell,ordertype,price,variety='NORMAL',exch_seg='NSE',triggerprice=0):
#     try:
#         orderparams = {
#             "variety": variety,
#             "tradingsymbol": symbol,
#             "symboltoken": token,
#             "transactiontype": buy_sell,
#             "exchange": exch_seg,
#             "ordertype": ordertype,
#             "producttype": "DELIVERY",
#             "duration": "DAY",
#             "price": price,
#             "squareoff": "0",
#             "stoploss": "0",
#             "quantity": qty,
#             "triggerprice":triggerprice
#             }
#         orderId=credentials.SMART_API_OBJ.placeOrder(orderparams)
#         print("The order id is: {}".format(orderId))
#     except Exception as e:
#         print("Order placement failed: {}".format(e.message))
#
#
#



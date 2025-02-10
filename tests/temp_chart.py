# temp/temp_chart.py
import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import mplfinance as mpf
from strategy.hln_calculator import HLNCalculator
from config.settings import TRADING_PARAMS


# اتصال به دیتابیس
def get_market_data():
    db_path = "database/vortex.db"
    query = "SELECT * FROM market_data ORDER BY date_time DESC LIMIT 1000"
    df = pd.read_sql(query, sqlite3.connect(db_path))
    df = df.sort_values(by="date_time")
    return df

# دریافت داده‌ها
market_data = get_market_data()

# محاسبه HLN خطوط
hln_calculator = HLNCalculator(
    market_data,
    tenkan_period=TRADING_PARAMS["TENKAN_PERIOD"],
    kijun_period=TRADING_PARAMS["KIJUN_PERIOD"],
    senkou_b_period=TRADING_PARAMS["SENKOU_B_PERIOD"],
    z_score=TRADING_PARAMS["Z_SCORE"],
    atr_multiplier=TRADING_PARAMS["ATR_MULTIPLIER"],
)
hln_points = hln_calculator.calculate_hln_lines()

# تبدیل نقاط به فرمت مورد نیاز
hln_highs = [(pd.Timestamp(market_data.iloc[idx]['date_time']).value, point) for idx, point in zip(hln_points[2], hln_points[0])]
hln_lows = [(pd.Timestamp(market_data.iloc[idx]['date_time']).value, point) for idx, point in zip(hln_points[2], hln_points[1])]

# ایجاد چارت کندل‌استیک
market_data['date_time'] = pd.to_datetime(market_data['date_time'])
market_data.set_index('date_time', inplace=True)

# افزودن سری کندل‌استیک
ohlc = market_data[['open', 'high', 'low', 'close']]

# افزودن خطوط Normal High و Normal Low
hln_highs = pd.DataFrame(hln_highs, columns=['date_time', 'High']).set_index('date_time')
hln_lows = pd.DataFrame(hln_lows, columns=['date_time', 'Low']).set_index('date_time')

# نمایش چارت
ap0 = [mpf.make_addplot(hln_highs['High'], color='g'),
       mpf.make_addplot(hln_lows['Low'], color='r')]

mpf.plot(ohlc, type='candle', style='charles', addplot=ap0, title='Candlestick Chart with HLN Lines', ylabel='Price')
plt.show()
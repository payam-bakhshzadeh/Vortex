import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import mplfinance as mpf
from utils.indicators import TechnicalIndicators
from config.settings import TRADING_PARAMS, ICHIMOKU_COLORS

# اتصال به دیتابیس
def get_market_data():
    db_path = os.path.join(os.path.dirname(__file__), '../vortex.db')
    query = "SELECT * FROM market_data ORDER BY date_time DESC LIMIT 1000"
    df = pd.read_sql(query, sqlite3.connect(db_path))
    df = df.sort_values(by="date_time")
    return df

# دریافت داده‌ها
market_data = get_market_data()

# ایجاد چارت کندل‌استیک
market_data['date_time'] = pd.to_datetime(market_data['date_time'])
market_data.set_index('date_time', inplace=True)

# افزودن سری کندل‌استیک
ohlc = market_data[['open', 'high', 'low', 'close']]

# محاسبات اندیکاتور Ichimoku
indicators = TechnicalIndicators()
ichimoku_components = indicators.calculate_ichimoku_components(
    market_data['high'],
    market_data['low'],
    market_data['close'],
    tenkan_period=TRADING_PARAMS["TENKAN_PERIOD"],
    kijun_period=TRADING_PARAMS["KIJUN_PERIOD"],
    senkou_b_period=TRADING_PARAMS["SENKOU_B_PERIOD"],
    ichimoku_shift=TRADING_PARAMS["ICHIMOKU_SHIFT"],
    chikou_shift=TRADING_PARAMS["CHIKOU_SHIFT"]
)

# افزودن خطوط Ichimoku به چارت
ap0 = [
    mpf.make_addplot(ichimoku_components['tenkan_sen'], color=ICHIMOKU_COLORS["TENKAN"]),
    mpf.make_addplot(ichimoku_components['kijun_sen'], color=ICHIMOKU_COLORS["KIJUN"]),
    mpf.make_addplot(ichimoku_components['senkou_span_a'], color=ICHIMOKU_COLORS["SENKOU_A"]),
    mpf.make_addplot(ichimoku_components['senkou_span_b'], color=ICHIMOKU_COLORS["SENKOU_B"]),
    mpf.make_addplot(ichimoku_components['chikou_span'], color=ICHIMOKU_COLORS["CHIKOU"]),
]

# نمایش چارت با پر کردن فضای بین Senkou Span A و Senkou Span B
mpf.plot(ohlc, type='candle', style='charles', addplot=ap0, title='Candlestick Chart with Ichimoku', ylabel='Price', fill_between=ichimoku_components["fill_between"])
plt.show()
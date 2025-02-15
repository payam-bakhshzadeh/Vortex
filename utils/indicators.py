import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from config.settings import TRADING_PARAMS, ICHIMOKU_COLORS

class TechnicalIndicators:
    @staticmethod
    def calculate_atr(
        high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
    ) -> pd.Series:
        """
        Calculate the Average True Range (ATR).

        Parameters:
            high (pd.Series): High prices.
            low (pd.Series): Low prices.
            close (pd.Series): Close prices.
            period (int): The period for ATR calculation (default is 14).

        Returns:
            pd.Series: ATR values.
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    @staticmethod
    def calculate_ichimoku_components(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        tenkan_period: int = TRADING_PARAMS["TENKAN_PERIOD"],
        kijun_period: int = TRADING_PARAMS["KIJUN_PERIOD"],
        senkou_b_period: int = TRADING_PARAMS["SENKOU_B_PERIOD"],
        ichimoku_shift: int = TRADING_PARAMS["ICHIMOKU_SHIFT"],
        chikou_shift: int = TRADING_PARAMS["CHIKOU_SHIFT"]
    ) -> Dict[str, Any]:
        """
        Calculate all Ichimoku components.

        Parameters:
            high (pd.Series): High prices.
            low (pd.Series): Low prices.
            close (pd.Series): Close prices.
            tenkan_period (int): The period for Tenkan-sen (default is 9).
            kijun_period (int): The period for Kijun-sen (default is 26).
            senkou_b_period (int): The period for Senkou Span B (default is 52).
            ichimoku_shift (int): The shift for Senkou Spans (default is 26).
            chikou_shift (int): The shift for Chikou Span (default is -26).

        Returns:
            Dict[str, Any]: Dictionary containing Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, Chikou Span, and fill_between parameters.
        """
        # محاسبه خطوط Tenkan-sen و Kijun-sen
        tenkan_high = high.rolling(window=tenkan_period).max()
        tenkan_low = low.rolling(window=tenkan_period).min()
        tenkan = (tenkan_high + tenkan_low) / 2

        kijun_high = high.rolling(window=kijun_period).max()
        kijun_low = low.rolling(window=kijun_period).min()
        kijun = (kijun_high + kijun_low) / 2

        # محاسبه خطوط Senkou Span A و Senkou Span B
        senkou_span_a = ((tenkan + kijun) / 2).shift(ichimoku_shift)
        senkou_span_b_high = high.rolling(window=senkou_b_period).max()
        senkou_span_b_low = low.rolling(window=senkou_b_period).min()
        senkou_span_b = ((senkou_span_b_high + senkou_span_b_low) / 2).shift(ichimoku_shift)

        # محاسبه خط Chikou Span
        chikou_span = close.shift(chikou_shift)

        # تنظیمات پر کردن فضای بین Senkou Span A و Senkou Span B
        fill_between = [
            dict(
                y1=senkou_span_a.values,
                y2=senkou_span_b.values,
                where=senkou_span_a >= senkou_span_b,
                alpha=0.3,
                facecolor=ICHIMOKU_COLORS["KOMU_ABOVE"],
                interpolate=True
            ),
            dict(
                y1=senkou_span_a.values,
                y2=senkou_span_b.values,
                where=senkou_span_a < senkou_span_b,
                alpha=0.3,
                facecolor=ICHIMOKU_COLORS["KOMU_BELOW"],
                interpolate=True
            )
        ]

        return {
            "tenkan_sen": tenkan,
            "kijun_sen": kijun,
            "senkou_span_a": senkou_span_a,
            "senkou_span_b": senkou_span_b,
            "chikou_span": chikou_span,
            "fill_between": fill_between
        }

    @staticmethod
    def detect_direction_change(series: pd.Series) -> pd.Series:
        """
        Detect direction changes in a series.

        Parameters:
            series (pd.Series): The series to analyze.

        Returns:
            pd.Series: Boolean series indicating direction changes.
        """
        diff = series.diff()
        return (diff * diff.shift(1)) < 0
    
    @staticmethod
    def detect_flat_state(series: pd.Series, threshold: float = 0.0001) -> pd.Series:
        """
        Detect flat states in a series.

        Parameters:
            series (pd.Series): The series to analyze.
            threshold (float): The threshold for detecting flat states (default is 0.0001).

        Returns:
            pd.Series: Boolean series indicating flat states.
        """
        return abs(series.diff()) < threshold
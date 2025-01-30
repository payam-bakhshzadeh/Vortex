# utils/indicators.py

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


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
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_b_period: int = 52,
    ) -> Dict[str, pd.Series]:
        """
        Calculate all Ichimoku components.

        Parameters:
            high (pd.Series): High prices.
            low (pd.Series): Low prices.
            tenkan_period (int): The period for Tenkan-sen (default is 9).
            kijun_period (int): The period for Kijun-sen (default is 26).
            senkou_b_period (int): The period for Senkou Span B (default is 52).

        Returns:
            Dict[str, pd.Series]: Dictionary containing Tenkan-sen, Kijun-sen, Senkou Span A, and Senkou Span B.
        """
        tenkan = (
            high.rolling(window=tenkan_period).max()
            + low.rolling(window=tenkan_period).min()
        ) / 2
        kijun = (
            high.rolling(window=kijun_period).max()
            + low.rolling(window=kijun_period).min()
        ) / 2
        senkou_span_a = (tenkan + kijun) / 2
        senkou_span_b = (
            high.rolling(window=senkou_b_period).max()
            + low.rolling(window=senkou_b_period).min()
        ) / 2

        return {
            "tenkan_sen": tenkan,
            "kijun_sen": kijun,
            "senkou_span_a": senkou_span_a,
            "senkou_span_b": senkou_span_b,
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

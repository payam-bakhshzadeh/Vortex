# strategy/hln_calculator.py

import pandas as pd
from typing import Tuple, List
from utils.indicators import TechnicalIndicators


class HLNCalculator:
    def __init__(
        self,
        data: pd.DataFrame,
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_b_period: int = 52,
        z_score: float = 1.96,
        atr_multiplier: float = 0.5,
    ):
        """
        Initialize the HLNCalculator with the given data and parameters.

        Parameters:
            data (pd.DataFrame): The DataFrame containing market data.
            tenkan_period (int): The period for Tenkan-sen (default is 9).
            kijun_period (int): The period for Kijun-sen (default is 26).
            senkou_b_period (int): The period for Senkou Span B (default is 52).
            z_score (float): The z-score for statistical analysis (default is 1.96).
            atr_multiplier (float): The ATR multiplier (default is 0.5).
        """
        self.data = data
        self.validate_data(data)
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period
        self.z_score = z_score
        self.atr_multiplier = atr_multiplier
        self.indicators = TechnicalIndicators()

    @staticmethod
    def validate_data(data: pd.DataFrame):
        """
        Validate the input DataFrame to ensure it contains the required columns and is not empty.

        Parameters:
            data (pd.DataFrame): The DataFrame to validate.

        Raises:
            ValueError: If the DataFrame does not contain the required columns or is empty.
        """
        required_columns = ["high", "low", "close"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data must contain columns: {required_columns}")
        if data.empty:
            raise ValueError("Empty dataset provided")

    def calculate_ichimoku(self) -> None:
        """
        Calculate Ichimoku components and add them to the DataFrame.
        """
        components = self.indicators.calculate_ichimoku_components(
            self.data["high"],
            self.data["low"],
            self.tenkan_period,
            self.kijun_period,
            self.senkou_b_period,
        )
        for key, value in components.items():
            self.data[key] = value

    def calculate_hln_lines(self) -> Tuple[List[float], List[float], List[int]]:
        """
        Calculate High-Low-Nadir (HLN) lines based on Ichimoku components and ATR.

        Returns:
            Tuple[List[float], List[float], List[int]]: Tuples containing HLN highs, lows, and timestamps.
        """
        self.calculate_ichimoku()

        atr_9 = self.indicators.calculate_atr(
            self.data["high"], self.data["low"], self.data["close"], self.tenkan_period
        )

        atr_26 = self.indicators.calculate_atr(
            self.data["high"], self.data["low"], self.data["close"], self.kijun_period
        )

        atr_52 = self.indicators.calculate_atr(
            self.data["high"],
            self.data["low"],
            self.data["close"],
            self.senkou_b_period,
        )

        major_points = pd.DataFrame(
            {
                "tenkan": self.indicators.detect_direction_change(
                    self.data["tenkan_sen"]
                ),
                "kijun": self.indicators.detect_direction_change(
                    self.data["kijun_sen"]
                ),
                "span_b": self.indicators.detect_direction_change(
                    self.data["senkou_span_b"]
                ),
            }
        )

        hln_highs, hln_lows, hln_timestamps = [], [], []

        for idx in range(len(self.data)):
            if major_points.iloc[idx].any():
                price_high = self.data["high"].iloc[idx]
                price_low = self.data["low"].iloc[idx]

                min_distance = max(
                    self.atr_multiplier * atr_9.iloc[idx],
                    self.atr_multiplier * atr_26.iloc[idx],
                    self.atr_multiplier * atr_52.iloc[idx],
                )

                if (
                    len(hln_highs) == 0
                    or abs(price_high - hln_highs[-1]) > min_distance
                ):
                    hln_highs.append(price_high)
                    hln_timestamps.append(idx)

                if len(hln_lows) == 0 or abs(price_low - hln_lows[-1]) > min_distance:
                    hln_lows.append(price_low)
                    hln_timestamps.append(idx)

        return hln_highs, hln_lows, hln_timestamps

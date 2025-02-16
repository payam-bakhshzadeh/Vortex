# strategy/hln_calculator.py
import pandas as pd
from typing import List, Tuple
from utils.indicators import TechnicalIndicators
from config.settings import TRADING_PARAMS

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
            high=self.data["high"],
            low=self.data["low"],
            close=self.data["close"],
            tenkan_period=self.tenkan_period,
            kijun_period=self.kijun_period,
            senkou_b_period=self.senkou_b_period,
            ichimoku_shift=TRADING_PARAMS["ICHIMOKU_SHIFT"],
            chikou_shift=TRADING_PARAMS["CHIKOU_SHIFT"]
        )
        for key, value in components.items():
            self.data[key] = value
    
    def calculate_hln_lines(self) -> Tuple[List[float], List[int]]:
        """
        Calculate High-Low-Nadir (HLN) lines based on Ichimoku components and ATR.
        Returns:
            Tuple[List[float], List[int]]: A tuple containing HLN points (highs and lows) and their timestamps.
        """
        self.calculate_ichimoku()
        # Calculate ATR for different periods
        atr_9 = self.indicators.calculate_atr(
            high=self.data["high"], 
            low=self.data["low"], 
            close=self.data["close"], 
            period=self.tenkan_period
        )
        atr_26 = self.indicators.calculate_atr(
            high=self.data["high"], 
            low=self.data["low"], 
            close=self.data["close"], 
            period=self.kijun_period
        )
        atr_52 = self.indicators.calculate_atr(
            high=self.data["high"], 
            low=self.data["low"], 
            close=self.data["close"], 
            period=self.senkou_b_period
        )
        # Detect direction changes in Ichimoku components
        major_points = pd.DataFrame(
            {
                "tenkan": self.indicators.detect_direction_change(self.data["tenkan_sen"]),
                "kijun": self.indicators.detect_direction_change(self.data["kijun_sen"]),
                "span_b": self.indicators.detect_direction_change(self.data["senkou_span_b"]),
            }
        )
        hln_points = []  # List to store HLN points (highs and lows)
        hln_timestamps = []  # List to store corresponding timestamps
        # Track the type of the last point added (None, "high", or "low")
        last_point_type = None
        for idx in range(len(self.data)):
            if major_points.iloc[idx].any():
                price_high = self.data["high"].iloc[idx]
                price_low = self.data["low"].iloc[idx]
                # Calculate the minimum distance based on ATR
                min_distance = max(
                    self.atr_multiplier * atr_9.iloc[idx],
                    self.atr_multiplier * atr_26.iloc[idx],
                    self.atr_multiplier * atr_52.iloc[idx],
                )
                # Add a high point if it meets the distance requirement and alternates with lows
                if (last_point_type != "high") and (
                    len(hln_points) == 0 or abs(
                        price_high - hln_points[-1]) > min_distance
                ):
                    hln_points.append(price_high)
                    hln_timestamps.append(idx)
                    last_point_type = "high"
                # Add a low point if it meets the distance requirement and alternates with highs
                elif (last_point_type != "low") and (
                    len(hln_points) == 0 or abs(
                        price_low - hln_points[-1]) > min_distance
                ):
                    hln_points.append(price_low)
                    hln_timestamps.append(idx)
                    last_point_type = "low"
        return hln_points, hln_timestamps
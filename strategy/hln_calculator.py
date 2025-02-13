import numpy as np
import pandas as pd
from typing import List, Tuple
from utils.indicators import TechnicalIndicators
from scipy.stats import norm

class HLNCalculator:
    def __init__(
        self,
        data: pd.DataFrame,
        tenkan_period: int = 9,
        confidence_level: float = 0.95,
    ):
        """
        Initialize the HLNCalculator with the given data and parameters.
        
        Parameters:
        data (pd.DataFrame): The DataFrame containing market data.
        tenkan_period (int): The period for Tenkan-sen (default is 9).
        confidence_level (float): Confidence level for dynamic tolerance (default is 0.95).
        """
        self.data = data
        self.validate_data(data)
        self.tenkan_period = tenkan_period
        self.confidence_level = confidence_level
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

    def detect_high_low_normal(self, period: int) -> Tuple[List[dict], List[dict]]:
        # محاسبه تغییرات قیمت
        self.data['Price_Change'] = self.data['close'].diff()
        # محاسبه میانگین و انحراف معیار تغییرات قیمت
        mean_change = self.data['Price_Change'].rolling(window=period).mean()
        std_dev = self.data['Price_Change'].rolling(window=period).std()
        
        # محاسبه Z-score برای سطح اطمینان مشخص
        z = norm.ppf(1 - (1 - self.confidence_level) / 2)  # دو طرفه
        
        # محاسبه تلرانس پویا
        tolerance = z * std_dev
        
        highs = []
        lows = []
        last_high = None
        last_low = None
        
        for i in range(len(self.data)):
            # تشخیص High Normal
            if last_low is not None and i - last_low['index'] <= period + tolerance[i]:
                if self.data['high'][i] > last_low['value']:
                    highs.append({'index': i, 'value': self.data['high'][i]})
                    last_high = {'index': i, 'value': self.data['high'][i]}
                    last_low = None
            
            # تشخیص Low Normal
            if last_high is not None and i - last_high['index'] <= period + tolerance[i]:
                if self.data['low'][i] < last_high['value']:
                    lows.append({'index': i, 'value': self.data['low'][i]})
                    last_low = {'index': i, 'value': self.data['low'][i]}
                    last_high = None
        
        return highs, lows

    def calculate_hln_lines(self) -> Tuple[List[float], List[int]]:
        """
        Calculate High-Low-Normal (HLN) lines based on Ichimoku components and dynamic tolerance.

        Returns:
            Tuple[List[float], List[int]]: A tuple containing HLN points (highs and lows) and their timestamps.
        """
        tenkan_highs, tenkan_lows = self.detect_high_low_normal(period=self.tenkan_period)

        hln_points = tenkan_highs + tenkan_lows
        hln_points = sorted(hln_points, key=lambda x: x['index'])
        
        hln_values = [point['value'] for point in hln_points]
        hln_timestamps = [point['index'] for point in hln_points]

        return hln_values, hln_timestamps
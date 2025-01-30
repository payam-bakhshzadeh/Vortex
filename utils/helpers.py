# utils/helpers.py

import pandas as pd
from datetime import datetime
from typing import Union, List, Dict


class DataHelper:
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate if a DataFrame contains all required columns.

        Parameters:
            df (pd.DataFrame): The DataFrame to validate.
            required_columns (List[str]): List of required column names.

        Returns:
            bool: True if all required columns are present, False otherwise.
        """
        return all(col in df.columns for col in required_columns)

    @staticmethod
    def format_datetime(dt: Union[str, datetime]) -> str:
        """
        Format a datetime object or string to a standard string format.

        Parameters:
            dt (Union[str, datetime]): The datetime object or string to format.

        Returns:
            str: Formatted datetime string in the format "%Y-%m-%d %H:%M:%S".
        """
        if isinstance(dt, str):
            dt = pd.to_datetime(dt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate_percentage_change(current: float, previous: float) -> float:
        """
        Calculate the percentage change between two values.

        Parameters:
            current (float): The current value.
            previous (float): The previous value.

        Returns:
            float: The percentage change. Returns 0 if the previous value is 0.
        """
        return ((current - previous) / previous) * 100 if previous != 0 else 0


class TimeframeConverter:
    @staticmethod
    def resample_ohlcv(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        Resample OHLCV data to a specified timeframe.

        Parameters:
            df (pd.DataFrame): The DataFrame containing OHLCV data with a 'datetime' column.
            timeframe (str): The target timeframe (e.g., '1H', 'D').

        Returns:
            pd.DataFrame: Resampled OHLCV data.
        """
        try:
            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            resampled = df.resample(timeframe).agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            resampled.reset_index(inplace=True)
            return resampled.dropna()
        except Exception as e:
            print(f"Error resampling OHLCV data: {e}")
            return pd.DataFrame()

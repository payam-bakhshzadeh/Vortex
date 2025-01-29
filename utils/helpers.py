import pandas as pd
from datetime import datetime
from typing import Union, List, Dict


class DataHelper:
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
        return all(col in df.columns for col in required_columns)

    @staticmethod
    def format_datetime(dt: Union[str, datetime]) -> str:
        if isinstance(dt, str):
            dt = pd.to_datetime(dt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate_percentage_change(current: float, previous: float) -> float:
        return ((current - previous) / previous) * 100 if previous != 0 else 0


class TimeframeConverter:
    @staticmethod
    def resample_ohlcv(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        resampled = df.resample(timeframe, on="datetime").agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
        return resampled.dropna()

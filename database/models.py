# database/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MarketData:
    """
    Represents a single row of market data.

    Attributes:
        datetime (datetime): The timestamp of the market data.
        open (float): The opening price of the market data.
        high (float): The highest price of the market data.
        low (float): The lowest price of the market data.
        close (float): The closing price of the market data.
        volume (int): The trading volume of the market data.
        id (Optional[int]): The unique identifier for the market data (optional).
    """
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    id: Optional[int] = None

@dataclass
class TradingSignal:
    """
    Represents a trading signal.

    Attributes:
        datetime (datetime): The timestamp of the trading signal.
        signal_type (str): The type of the trading signal (e.g., 'buy', 'sell').
        price (float): The price at which the signal is generated.
        strength (float): The strength of the trading signal.
        id (Optional[int]): The unique identifier for the trading signal (optional).
    """
    datetime: datetime
    signal_type: str
    price: float
    strength: float
    id: Optional[int] = None
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MarketData:
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    id: Optional[int] = None


@dataclass
class TradingSignal:
    datetime: datetime
    signal_type: str
    price: float
    strength: float
    id: Optional[int] = None

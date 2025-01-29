import unittest
import pandas as pd
import numpy as np
from strategy.strategy import VortexStrategy
from strategy.hln_calculator import HLNCalculator
from utils.indicators import TechnicalIndicators


class TestVortexStrategy(unittest.TestCase):
    def setUp(self):
        # Create more realistic market data with price movements
        periods = 100
        base_price = 100
        np.random.seed(42)  # For reproducible results

        # Generate prices with some volatility
        price_changes = np.random.normal(0, 1, periods)
        closes = base_price + np.cumsum(price_changes)
        highs = closes + np.random.uniform(0, 2, periods)
        lows = closes - np.random.uniform(0, 2, periods)

        self.test_data = pd.DataFrame(
            {
                "datetime": pd.date_range(
                    start="2024-01-01", periods=periods, freq="h"
                ),
                "open": closes - np.random.uniform(0, 1, periods),
                "high": highs,
                "low": lows,
                "close": closes,
                "volume": np.random.randint(1000, 10000, periods),
            }
        )

        self.strategy = VortexStrategy()
        self.indicators = TechnicalIndicators()

    def test_indicator_calculations(self):
        # Calculate ATR with sufficient data points
        atr = self.indicators.calculate_atr(
            self.test_data["high"],
            self.test_data["low"],
            self.test_data["close"],
            period=14,
        )
        # Skip first 14 values due to rolling window
        atr = atr[14:]
        self.assertTrue(len(atr) > 0)
        self.assertTrue(all(~pd.isna(atr)))

    def test_hln_calculation(self):
        self.strategy.initialize(self.test_data)
        signals = self.strategy.calculate_signals()

        self.assertIsNotNone(signals["hln_highs"])
        self.assertIsNotNone(signals["hln_lows"])
        self.assertTrue(len(signals["timestamps"]) > 0)

        # Verify HLN lines are properly ordered
        if len(signals["hln_highs"]) > 1:
            self.assertTrue(
                all(
                    signals["hln_highs"][i] >= signals["hln_lows"][i]
                    for i in range(len(signals["hln_highs"]))
                )
            )

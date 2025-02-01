# tests/test_strategy.py

import unittest
import pandas as pd
import numpy as np
from strategy.strategy import VortexStrategy
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
        atr = self.indicators.calculate_atr(
            self.test_data["high"],
            self.test_data["low"],
            self.test_data["close"],
            period=14,
        )
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

    def test_strategy_initialization(self):
        self.strategy.initialize(self.test_data)
        self.assertIsNotNone(self.strategy.hln_calculator)

    def test_strategy_with_empty_data(self):
        empty_data = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.strategy.initialize(empty_data)

    def test_strategy_with_invalid_config(self):
        invalid_config = {
            "tenkan_period": -1,
            "kijun_period": 26,
            "senkou_b_period": 52,
            "z_score": 1.96,
            "atr_multiplier": 0.5,
        }
        with self.assertRaises(ValueError):
            VortexStrategy(config=invalid_config)

if __name__ == "__main__":
    unittest.main()

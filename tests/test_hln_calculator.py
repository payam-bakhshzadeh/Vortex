# tests/test_hln_calculator.py

import unittest
import pandas as pd
import numpy as np
from strategy.hln_calculator import HLNCalculator
from utils.indicators import TechnicalIndicators

class TestHLNCalculator(unittest.TestCase):
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

        self.hln_calculator = HLNCalculator(self.test_data)

    def test_calculate_ichimoku(self):
        self.hln_calculator.calculate_ichimoku()
        required_columns = ["tenkan_sen", "kijun_sen", "senkou_span_a", "senkou_span_b"]
        self.assertTrue(all(col in self.test_data.columns for col in required_columns))

    def test_calculate_hln_lines(self):
        hln_highs, hln_lows, timestamps = self.hln_calculator.calculate_hln_lines()
        self.assertIsNotNone(hln_highs)
        self.assertIsNotNone(hln_lows)
        self.assertTrue(len(timestamps) > 0)

        # Verify HLN lines are properly ordered
        if len(hln_highs) > 1:
            self.assertTrue(
                all(
                    hln_highs[i] >= hln_lows[i]
                    for i in range(len(hln_highs))
                )
            )

if __name__ == "__main__":
    unittest.main()

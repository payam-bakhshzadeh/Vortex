from typing import Dict, Any
from .hln_calculator import HLNCalculator
from utils.indicators import TechnicalIndicators


class VortexStrategy:
    def __init__(self, config: Dict[str, Any] = None):
        self.validate_config(config)
        self.config = config or {
            "tenkan_period": 9,
            "kijun_period": 26,
            "senkou_b_period": 52,
            "z_score": 1.96,
            "atr_multiplier": 0.5,
        }
        self.hln_calculator = None
        self.indicators = TechnicalIndicators()

    def validate_config(self, config: Dict[str, Any]):
        if config:
            if any(
                value <= 0
                for value in [
                    config.get("tenkan_period", 9),
                    config.get("kijun_period", 26),
                    config.get("senkou_b_period", 52),
                ]
            ):
                raise ValueError("Periods must be positive numbers")

    def initialize(self, market_data):
        if market_data.empty:
            raise ValueError("Empty market data provided")
        self.market_data = market_data
        self.hln_calculator = HLNCalculator(
            market_data,
            tenkan_period=self.config["tenkan_period"],
            kijun_period=self.config["kijun_period"],
            senkou_b_period=self.config["senkou_b_period"],
            z_score=self.config["z_score"],
            atr_multiplier=self.config["atr_multiplier"],
        )

    def calculate_signals(self):
        if not self.hln_calculator:
            raise ValueError("Strategy not initialized with market data")

        hln_highs, hln_lows, timestamps = self.hln_calculator.calculate_hln_lines()

        return {"hln_highs": hln_highs, "hln_lows": hln_lows, "timestamps": timestamps}

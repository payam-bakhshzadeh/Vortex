# strategy/strategy.py
from typing import Dict, Any, List, Tuple
from .hln_calculator import HLNCalculator
from utils.indicators import TechnicalIndicators
import pandas as pd


class VortexStrategy:
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the VortexStrategy with the given configuration.
        Parameters:
        config (Dict[str, Any]): Configuration parameters for the strategy.
        """
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
        """
        Validate the configuration parameters.
        Parameters:
        config (Dict[str, Any]): Configuration parameters to validate.
        Raises:
        ValueError: If any period is not a positive number.
        """
        if config:
            for key in ["tenkan_period", "kijun_period", "senkou_b_period"]:
                value = config.get(key, 0)
                if value <= 0:
                    raise ValueError(f"{key} must be a positive number")

    def initialize(self, market_data: pd.DataFrame):
        """
        Initialize the strategy with market data.
        Parameters:
        market_data (pd.DataFrame): The DataFrame containing market data.
        Raises:
        ValueError: If the market data is empty.
        """
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

    def calculate_signals(self) -> Dict[str, List[Any]]:
        """
        Calculate trading signals based on the market data.

        Returns:
            Dict[str, List[Any]]: A dictionary containing HLN points and timestamps.

        Raises:
            ValueError: If the strategy is not initialized with market data.
        """
        if not self.hln_calculator:
            raise ValueError("Strategy not initialized with market data")

        hln_points, timestamps = self.hln_calculator.calculate_hln_lines()

        return {"hln_points": hln_points, "timestamps": timestamps}

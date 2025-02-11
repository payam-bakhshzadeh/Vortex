# Trading Parameters
TRADING_PARAMS = {
    "TENKAN_PERIOD": 9,
    "KIJUN_PERIOD": 26,
    "SENKOU_B_PERIOD": 52,
    "ATR_MULTIPLIER": 0.5,
    "Z_SCORE": 1.96,
    "ICHIMOKU_SHIFT": 26,  # افزودن شیفت ایچی موکو
    "CHIKOU_SHIFT": -26,   # افزودن شیفت چیکو اسپن
}

# Ichimoku Colors
ICHIMOKU_COLORS = {
    "TENKAN": "red",
    "KIJUN": "blue",
    "SENKOU_A": "yellow",
    "SENKOU_B": "black",
    "CHIKOU": "black",
    "KOMU_ABOVE": "green",  # رنگ فضای بالای Komu
    "KOMU_BELOW": "red"     # رنگ فضای پایین Komu
}

# Database Configuration
DATABASE = {"NAME": "vortex.db", "PATH": "database/"}

# GUI Settings
GUI = {
    "WINDOW_TITLE": "Vortex Trading System",
    "WINDOW_SIZE": (800, 600),
    "THEME": "light",
}

# Logging Configuration
LOGGING = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}
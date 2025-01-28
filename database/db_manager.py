import sqlite3
import pandas as pd


class DatabaseManager:
    def __init__(self, db_name: str = "market_data.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER
                )
            """
            )

    def store_market_data(self, df: pd.DataFrame):
        with sqlite3.connect(self.db_name) as conn:
            df.to_sql("market_data", conn, if_exists="replace", index=False)

    def append_market_data(self, df: pd.DataFrame):
        with sqlite3.connect(self.db_name) as conn:
            df.to_sql("market_data", conn, if_exists="append", index=False)

    def get_market_data(self) -> pd.DataFrame:
        with sqlite3.connect(self.db_name) as conn:
            query = "SELECT * FROM market_data ORDER BY datetime"
            df = pd.read_sql_query(query, conn)
            df["datetime"] = pd.to_datetime(df["datetime"])
            return df

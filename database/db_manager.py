import sqlite3
import pandas as pd
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_name=":memory:"):
        self.db_name = db_name
        self._create_tables()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def _create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS market_data (
                    datetime TEXT PRIMARY KEY,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER
                )
                """
            )
            conn.commit()

    def drop_market_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS market_data")
            conn.commit()
            
    def store_market_data(self, df: pd.DataFrame):
        print("Storing data in database:", df)  # Debugging statement
        with self.get_connection() as conn:
            print("Data before storing:", df)  # Debugging statement
            df = df.copy()
            df.columns = df.columns.str.lower()
            df.to_sql("market_data", conn, if_exists="replace", index=False)
            conn.commit()
        print("Data stored successfully.")  # Debugging statement
    
    def get_market_data(self) -> pd.DataFrame:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='market_data'"
            )
            if not cursor.fetchone():
                return pd.DataFrame()

            df = pd.read_sql_query("SELECT * FROM market_data ORDER BY datetime", conn)
            if not df.empty:
                df["datetime"] = pd.to_datetime(df["datetime"])
            return df

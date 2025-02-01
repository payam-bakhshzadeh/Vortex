import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(db_name=":memory:")

    @patch('sqlite3.connect')
    def test_get_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        with self.db_manager.get_connection() as conn:
            self.assertEqual(conn, mock_conn)
        mock_conn.close.assert_called_once()

    def test_create_tables(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='market_data'")
            table_exists = cursor.fetchone()
            self.assertIsNotNone(table_exists)

    def test_drop_market_data(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='market_data'")
            table_exists = cursor.fetchone()
            self.assertIsNotNone(table_exists)

        self.db_manager.drop_market_data()

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='market_data'")
            table_exists = cursor.fetchone()
            self.assertIsNone(table_exists)

    def test_store_market_data(self):
        df = pd.DataFrame({
            'Date': ['2023-10-01'],
            'Time': ['10:00:00'],
            'Open': [100.0],
            'High': [105.0],
            'Low': [95.0],
            'Close': [102.0],
            'Volume': [1000]
        })

        self.db_manager.store_market_data(df)

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM market_data")
            stored_data = cursor.fetchall()
            self.assertEqual(len(stored_data), 1)
            self.assertEqual(stored_data[0], ('2023-10-01', '10:00:00',
                             100.0, 105.0, 95.0, 102.0, 1000, '2023-10-01 10:00:00'))

    def test_get_market_data(self):
        df = pd.DataFrame({
            'Date': ['2023-10-01'],
            'Time': ['10:00:00'],
            'Open': [100.0],
            'High': [105.0],
            'Low': [95.0],
            'Close': [102.0],
            'Volume': [1000]
        })

        self.db_manager.store_market_data(df)

        retrieved_data = self.db_manager.get_market_data()
        self.assertFalse(retrieved_data.empty)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data.iloc[0]['open'], 100.0)


if __name__ == '__main__':
    unittest.main()

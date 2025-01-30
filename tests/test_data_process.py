# tests/test_data_process.py

import unittest
import pandas as pd
from unittest.mock import MagicMock, patch
from data.data_processor import DataProcessor
from database.db_manager import DatabaseManager


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a mock DatabaseManager and DataProcessor.
        """
        self.db_manager = MagicMock(spec=DatabaseManager)
        self.data_processor = DataProcessor(self.db_manager)
        self.data_processor.set_file_path("test_data.csv")
        self.data_processor.set_mode("append")

        # Sample data for testing
        self.sample_data = pd.DataFrame(
            {
                "datetime": ["2023-10-01 10:00:00", "2023-10-01 11:00:00"],
                "open": [100, 101],
                "high": [105, 106],
                "low": [99, 100],
                "close": [102, 103],
                "volume": [1000, 1500],
            }
        )

    @patch("pandas.read_csv")
    def test_check_duplicates_no_existing_data(self, mock_read_csv):
        """
        Test check_duplicates method when there is no existing data in the database.
        """
        mock_read_csv.return_value = self.sample_data
        self.db_manager.get_market_data.return_value = pd.DataFrame()

        result = self.data_processor.check_duplicates("test_data.csv")
        self.assertFalse(result)

    @patch("pandas.read_csv")
    def test_check_duplicates_with_existing_data_no_duplicates(self, mock_read_csv):
        """
        Test check_duplicates method when there is existing data with no duplicates.
        """
        mock_read_csv.return_value = self.sample_data
        self.db_manager.get_market_data.return_value = pd.DataFrame(
            {
                "datetime": ["2023-10-01 09:00:00"],
                "open": [98],
                "high": [100],
                "low": [97],
                "close": [99],
                "volume": [800],
            }
        )

        result = self.data_processor.check_duplicates("test_data.csv")
        self.assertFalse(result)

    @patch("pandas.read_csv")
    def test_check_duplicates_with_existing_data_with_duplicates(self, mock_read_csv):
        """
        Test check_duplicates method when there is existing data with duplicates.
        """
        mock_read_csv.return_value = self.sample_data
        self.db_manager.get_market_data.return_value = self.sample_data

        result = self.data_processor.check_duplicates("test_data.csv")
        self.assertTrue(result)

    @patch("pandas.read_csv")
    def test_process_and_save_append_mode(self, mock_read_csv):
        """
        Test process_and_save method in append mode.
        """
        mock_read_csv.return_value = self.sample_data
        self.db_manager.get_market_data.return_value = pd.DataFrame()

        self.data_processor.process_and_save()

        self.db_manager.store_market_data.assert_called_once_with(self.sample_data)

    @patch("pandas.read_csv")
    def test_process_and_save_replace_mode(self, mock_read_csv):
        """
        Test process_and_save method in replace mode.
        """
        mock_read_csv.return_value = self.sample_data
        self.db_manager.get_market_data.return_value = pd.DataFrame(
            {
                "datetime": ["2023-10-01 09:00:00"],
                "open": [98],
                "high": [100],
                "low": [97],
                "close": [99],
                "volume": [800],
            }
        )
        self.data_processor.set_mode("replace")

        self.data_processor.process_and_save()

        self.db_manager.drop_market_data.assert_called_once()
        self.db_manager.store_market_data.assert_called_once_with(self.sample_data)


if __name__ == "__main__":
    unittest.main()

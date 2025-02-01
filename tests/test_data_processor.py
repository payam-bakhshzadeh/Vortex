import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data.data_processor import DataProcessor
from database.db_manager import DatabaseManager


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.db_manager = MagicMock(spec=DatabaseManager)
        self.data_processor = DataProcessor(self.db_manager)

    def test_set_file_path(self):
        file_path = "path/to/file.csv"
        self.data_processor.set_file_path(file_path)
        self.assertEqual(self.data_processor.file_path, file_path)

    @patch('pandas.read_csv')
    def test_check_duplicates(self, mock_read_csv):
        existing_data = pd.DataFrame({
            'date': ['2023-10-01'],
            'time': ['10:00:00'],
            'date_time': ['2023-10-01 10:00:00']
        })
        self.db_manager.get_market_data.return_value = existing_data

        new_data = pd.DataFrame({
            'Date': ['2023-10-01'],
            'Time': ['10:00:00'],
            'date_time': ['2023-10-01 10:00:00']
        })
        mock_read_csv.return_value = new_data

        has_duplicates = self.data_processor.check_duplicates(
            "path/to/file.csv")
        self.assertTrue(has_duplicates)

    @patch('pandas.read_csv')
    def test_process_and_save(self, mock_read_csv):
        data = pd.DataFrame({
            'Date': ['2023-10-01'],
            'Time': ['10:00:00'],
            'Open': [100.0],
            'High': [105.0],
            'Low': [95.0],
            'Close': [102.0],
            'Volume': [1000]
        })
        mock_read_csv.return_value = data
        self.data_processor.set_file_path("path/to/file.csv")

        self.data_processor.process_and_save()

        self.db_manager.drop_market_data.assert_called_once()
        self.db_manager.store_market_data.assert_called_once_with(data)


if __name__ == '__main__':
    unittest.main()

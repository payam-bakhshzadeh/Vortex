import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager
from data.data_processor import DataProcessor
import pandas as pd


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.db_manager = MagicMock(spec=DatabaseManager)
        self.data_processor = MagicMock(spec=DataProcessor)
        self.data_processor.db_manager = self.db_manager
        self.main_window = MainWindow(self.db_manager)

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_upload_csv(self, mock_get_open_file_name):
        file_path = "path/to/file.csv"
        mock_get_open_file_name.return_value = (file_path, "")
        self.data_processor.check_duplicates.return_value = False

        self.main_window.upload_csv()

        self.data_processor.set_file_path.assert_called_once_with(file_path)
        self.data_processor.process_and_save.assert_called_once()

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_upload_csv_with_duplicates(self, mock_get_open_file_name):
        file_path = "path/to/file.csv"
        mock_get_open_file_name.return_value = (file_path, "")
        self.data_processor.check_duplicates.return_value = True
        self.main_window.handle_duplicates.return_value = True

        self.main_window.upload_csv()

        self.data_processor.set_file_path.assert_called_once_with(file_path)
        self.data_processor.process_and_save.assert_called_once()

    def test_check_database_status(self):
        data = pd.DataFrame({
            'date_time': pd.to_datetime(['2023-10-01 10:00:00', '2023-10-01 11:00:00'])
        })
        self.db_manager.get_market_data.return_value = data

        self.main_window.check_database_status()

        self.assertEqual(self.main_window.status_label.text(),
                         "Database Status: Market data available\nFrom: 2023-10-01 10:00:00\nTo: 2023-10-01 11:00:00")


if __name__ == '__main__':
    unittest.main()

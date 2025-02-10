# gui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from data.data_processor import DataProcessor
from .styles import StyleSheet
from .dialogs import DataRangeDialog
from utils.file_handler import FileHandler
from database.db_manager import DatabaseManager
from strategy.strategy import VortexStrategy
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        """
        Initialize the MainWindow with a database manager.
        Parameters:
        db_manager (DatabaseManager): The database manager instance.
        """
        super().__init__()
        self.db_manager = db_manager
        self.data_processor = DataProcessor(db_manager)
        self.file_handler = FileHandler("output.json")  # اضافه شده
        self.strategy = VortexStrategy()
        self.setup_ui()
        self.check_database_status()

    def setup_ui(self):
        """
        Set up the user interface for the MainWindow.
        """
        self.setWindowTitle("Vortex Trading System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(StyleSheet.MAIN_WINDOW)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top controls
        controls_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.upload_btn.setStyleSheet(StyleSheet.BUTTON)
        controls_layout.addWidget(self.upload_btn)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_commands)
        self.submit_btn.setStyleSheet(StyleSheet.BUTTON)
        controls_layout.addWidget(self.submit_btn)

        main_layout.addLayout(controls_layout)

        # JSON File Save Path
        json_path_layout = QHBoxLayout()
        self.json_path_label = QLabel("JSON File Save Path:")
        self.json_path_label.setStyleSheet(StyleSheet.LABEL)
        json_path_layout.addWidget(self.json_path_label)

        self.json_path_edit = QLineEdit(self.file_handler.current_path)
        self.json_path_edit.setStyleSheet(StyleSheet.LINE_EDIT)
        json_path_layout.addWidget(self.json_path_edit)

        main_layout.addLayout(json_path_layout)

        # Status display
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(StyleSheet.STATUS_LABEL)
        main_layout.addWidget(self.status_label)

    def check_database_status(self):
        """
        Check the status of the database and update the status label accordingly.
        """
        data = self.db_manager.get_market_data()
        if data.empty:
            self.status_label.setText(
                "Database Status: No market data available. Please upload data."
            )
            return
        start_date = data["date_time"].min().strftime("%Y-%m-%d %H:%M:%S")
        end_date = data["date_time"].max().strftime("%Y-%m-%d %H:%M:%S")
        self.status_label.setText(
            f"Database Status: Market data available\nFrom: {start_date}\nTo: {end_date}"
        )

    def upload_csv(self):
        """
        Open a file dialog to upload a CSV file and handle duplicates if found.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                duplicates = self.data_processor.check_duplicates(file_path)
                if duplicates:
                    response = self.handle_duplicates(file_path)
                    if response:
                        self.data_processor.set_file_path(file_path)
                        self.process_data()
                else:
                    self.data_processor.set_file_path(file_path)
                    self.process_data()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error processing file: {str(e)}"
                )

    def handle_duplicates(self, file_path):
        """
        Handle duplicate data by showing a dialog and returning the user's response.
        Parameters:
        file_path (str): The path to the CSV file.
        Returns:
        bool: True if the user chose to proceed, False otherwise.
        """
        dialog = DataRangeDialog(self)
        return dialog.exec_()

    def process_data(self):
        """
        Process and save the uploaded data.
        """
        try:
            self.data_processor.process_and_save()
            data = self.db_manager.get_market_data()
            record_count = len(data)
            QMessageBox.information(
                self,
                "Success",
                f"Data processed successfully!\nRecords saved: {record_count}",
            )
            self.check_database_status()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error processing data: {str(e)}"
            )

    def submit_commands(self):
        """
        Handle the submit button click to write commands to a JSON file.
        """
        try:
            market_data = self.db_manager.get_market_data()
            self.strategy.initialize(market_data)
            signals = self.strategy.calculate_signals()

            json_path = self.json_path_edit.text()
            self.file_handler.write_json(signals, json_path)
            QMessageBox.information(
                self,
                "Success",
                f"JSON file created successfully at {json_path}",
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error creating JSON file: {str(e)}"
            )

    def get_current_timestamp(self) -> str:
        """
        Get the current timestamp in a formatted string.
        Returns:
        str: The current timestamp.
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
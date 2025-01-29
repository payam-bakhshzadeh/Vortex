from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from data.data_processor import DataProcessor
from .styles import StyleSheet
from .dialogs import DataRangeDialog


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.data_processor = DataProcessor(db_manager)
        self.setup_ui()
        self.check_database_status()

    def setup_ui(self):
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
        self.submit_btn.clicked.connect(self.process_data)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setStyleSheet(StyleSheet.BUTTON)
        controls_layout.addWidget(self.submit_btn)

        main_layout.addLayout(controls_layout)

        # Status display
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(StyleSheet.STATUS_LABEL)
        main_layout.addWidget(self.status_label)

    def check_database_status(self):
        data = self.db_manager.get_market_data()

        if data.empty:
            self.status_label.setText(
                "Database Status: No market data available. Please upload data."
            )
            return

        start_date = data["datetime"].min().strftime("%Y-%m-%d %H:%M:%S")
        end_date = data["datetime"].max().strftime("%Y-%m-%d %H:%M:%S")
        self.status_label.setText(
            f"Database Status: Market data available\nFrom: {start_date}\nTo: {end_date}"
        )

    def upload_csv(self):
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
                        self.submit_btn.setEnabled(True)
                else:
                    self.data_processor.set_file_path(file_path)
                    self.submit_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error processing file: {str(e)}")

    def handle_duplicates(self, file_path):
        dialog = DataRangeDialog(self)
        return dialog.exec_()

    def process_data(self):
        try:
            self.data_processor.process_and_save()
            QMessageBox.information(self, "Success", "Data processed successfully!")
            self.submit_btn.setEnabled(False)
            self.check_database_status()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing data: {str(e)}")

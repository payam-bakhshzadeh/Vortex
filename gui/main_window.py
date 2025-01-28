from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel,
)
from PyQt5.QtCore import Qt
from data.data_processor import DataProcessor


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.data_processor = DataProcessor(db_manager)
        self.setup_ui()
        self.check_database_status()
        data = self.db_manager.get_market_data()
        if not data.empty:
            self.submit_btn.setEnabled(True)

    def setup_ui(self):
        self.setWindowTitle("Market Data Analysis")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.upload_btn = QPushButton("Upload CSV", self)
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            """
            QLabel {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
        """
        )
        layout.addWidget(self.status_label)

        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.clicked.connect(self.process_data)
        self.submit_btn.setEnabled(False)
        layout.addWidget(self.submit_btn)

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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Duplicate data found in the uploaded file!")
        msg.setInformativeText("How would you like to proceed?")
        msg.setWindowTitle("Duplicate Data Detected")

        replace_btn = msg.addButton("Complete Replacement", QMessageBox.ActionRole)
        new_only_btn = msg.addButton("Save Only New Data", QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)

        msg.exec_()
        clicked_button = msg.clickedButton()

        if clicked_button == replace_btn:
            self.data_processor.set_mode("replace")
            return True
        elif clicked_button == new_only_btn:
            self.data_processor.set_mode("new_only")
            return True
        return False

    def check_database_status(self):
        data = self.db_manager.get_market_data()

        if data.empty:
            self.status_label.setText(
                "Database Status: No market data available. Please upload data."
            )
            return

        datetime_col = "datetime" if "datetime" in data.columns else "DateTime"

        start_date = data[datetime_col].min().strftime("%Y-%m-%d %H:%M:%S")
        end_date = data[datetime_col].max().strftime("%Y-%m-%d %H:%M:%S")
        status_text = (
            f"Database Status: Market data available from {start_date} to {end_date}"
        )
        self.status_label.setText(status_text)

    def process_data(self):
        try:
            self.data_processor.process_and_save()
            QMessageBox.information(self, "Success", "Data processed successfully!")
            self.check_database_status()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing data: {str(e)}")

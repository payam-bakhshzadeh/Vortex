import sys
from PyQt5.QtWidgets import QApplication
from database.db_manager import DatabaseManager
from gui.main_window import MainWindow
from strategy.hln_calculator import HLNCalculator
from utils.file_handler import FileHandler
import pandas as pd

def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    window = MainWindow(db)
    window.show()
    
    # Load market data from the database
    market_data = db.load_market_data()
    
    # Initialize HLNCalculator with market data
    hln_calculator = HLNCalculator(data=market_data)
    
    # Calculate HLN lines
    hln_values, hln_timestamps = hln_calculator.calculate_hln_lines()
    
    # Prepare data for JSON output
    hln_output = {
        "hln_values": hln_values,
        "hln_timestamps": hln_timestamps
    }
    
    # Initialize FileHandler and write JSON output
    file_handler = FileHandler()
    json_file_path = file_handler.write_json(hln_output)
    
    print(f"HLN data has been written to {json_file_path}")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
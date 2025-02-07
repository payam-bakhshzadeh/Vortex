# api/api_server.py
import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
import pandas as pd
from database.db_manager import DatabaseManager
from strategy.strategy import VortexStrategy
from data.data_processor import DataProcessor


app = Flask(__name__)
db_manager = DatabaseManager()


@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        file = request.files['file']
        data = pd.read_csv(file)
        data_processor = DataProcessor(db_manager)
        data_processor.set_file_path(file.filename)
        data_processor.process_and_save()
        return jsonify({"status": "success", "message": "Data uploaded and processed successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/calculate_signals', methods=['GET'])
def calculate_signals():
    try:
        market_data = db_manager.get_market_data()
        strategy = VortexStrategy()
        strategy.initialize(market_data)
        signals = strategy.calculate_signals()
        return jsonify(signals), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

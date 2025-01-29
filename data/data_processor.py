import pandas as pd


class DataProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.file_path = None
        self.mode = "append"  # default mode

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_mode(self, mode):
        self.mode = mode

    def check_duplicates(self, file_path):
        # Read new data and check against existing data in database
        new_data = pd.read_csv(file_path)
        existing_data = self.db_manager.get_market_data()

        if existing_data.empty:
            return False

        return not existing_data.merge(new_data).empty

    def process_and_save(self):
        # Read and process the data
        data = pd.read_csv(self.file_path)
        print("Data read from CSV:", data)  # Debugging statement

        if self.mode == "replace":
            # Drop existing data from database
            self.db_manager.drop_market_data()

        # Store the processed data
        print("Attempting to store the following data:", data)  # Debugging statement
        self.db_manager.store_market_data(data)
        print("Data storage attempt completed.")  # Debugging statement
        # Retrieve and print stored data for verification
        stored_data = self.db_manager.get_market_data()
        print("Data retrieved from database:", stored_data)  # Debugging statement

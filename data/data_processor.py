# data/data_processor.py

import pandas as pd


class DataProcessor:
    def __init__(self, db_manager):
        """
        Initializes the DataProcessor with a database manager.

        Parameters:
            db_manager (DatabaseManager): An instance of DatabaseManager to handle database operations.
        """
        self.db_manager = db_manager
        self.file_path = None
        self.mode = "append"  # Default mode

    def set_file_path(self, file_path):
        """
        Sets the file path for the data file.

        Parameters:
            file_path (str): The path to the CSV file containing market data.
        """
        self.file_path = file_path

    def set_mode(self, mode):
        """
        Sets the mode for processing data (either 'append' or 'replace').

        Parameters:
            mode (str): The mode for processing data.
        """
        self.mode = mode

    def check_duplicates(self, file_path):
        """
        Checks for duplicates in the new data compared to existing data in the database.

        Parameters:
            file_path (str): The path to the CSV file containing new market data.

        Returns:
            bool: True if duplicates are found, False otherwise.
        """
        try:
            new_data = pd.read_csv(file_path)
            # Rename columns to match database schema
            new_data.rename(
                columns={
                    "Date": "datetime",
                    "Time": "time",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                },
                inplace=True,
            )
            new_data["datetime"] = pd.to_datetime(
                new_data["datetime"] + " " + new_data["time"]
            )
            new_data.drop(columns=["time"], inplace=True)

            existing_data = self.db_manager.get_market_data()

            if existing_data.empty:
                return False

            # Check for duplicates by merging new data with existing data
            merged_data = pd.merge(
                new_data, existing_data, on=["datetime"], how="inner"
            )
            return not merged_data.empty
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False

    def process_and_save(self):
        """
        Reads, processes, and saves market data to the database.
        """
        try:
            if not self.file_path:
                raise ValueError("File path not set.")

            # Read the data from the CSV file
            data = pd.read_csv(self.file_path)
            # Rename columns to match database schema
            data.rename(
                columns={
                    "Date": "datetime",
                    "Time": "time",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                },
                inplace=True,
            )
            data["datetime"] = pd.to_datetime(data["datetime"] + " " + data["time"])
            data.drop(columns=["time"], inplace=True)
            print("Data read from CSV:", data)  # Debugging statement

            if self.mode == "replace":
                # Drop existing data from the database
                self.db_manager.drop_market_data()
                print("Existing data dropped from database.")  # Debugging statement

            # Store the processed data
            print(
                "Attempting to store the following data:", data
            )  # Debugging statement
            self.db_manager.store_market_data(data)
            print("Data storage attempt completed.")  # Debugging statement

            # Retrieve and print stored data for verification
            stored_data = self.db_manager.get_market_data()
            print("Data retrieved from database:", stored_data)  # Debugging statement
        except Exception as e:
            print(f"Error processing and saving data: {e}")

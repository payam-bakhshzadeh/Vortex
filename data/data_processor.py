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

    def set_file_path(self, file_path):
        """
        Sets the file path for the data file.

        Parameters:
            file_path (str): The path to the CSV file containing market data.
        """
        self.file_path = file_path

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
            existing_data = self.db_manager.get_market_data()

            # Drop rows with NaN values in 'Date' or 'Time' columns
            new_data = new_data.dropna(subset=["Date", "Time"])
            existing_data = existing_data.dropna(subset=["date", "time"])

            if existing_data.empty:
                return False

            # Combine date and time columns to create date_time for new_data
            new_data["date_time"] = (
                new_data["Date"].astype(str) + " " + new_data["Time"].astype(str)
            )

            # Combine date and time columns to create date_time for existing_data
            if "date" in existing_data.columns and "time" in existing_data.columns:
                existing_data["date_time"] = (
                    existing_data["date"].astype(str)
                    + " "
                    + existing_data["time"].astype(str)
                )

            # Check for duplicates by merging new data with existing data
            merged_data = pd.merge(
                new_data, existing_data, on=["date_time"], how="inner"
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
                raise ValueError("File path is not set.")

            # Read the data from the CSV file
            data = pd.read_csv(self.file_path)
            print("Data read from CSV:", data)  # Debugging statement

            # Drop rows with NaN values in 'Date' or 'Time' columns
            data = data.dropna(subset=["Date", "Time"])

            # Combine date and time columns to create date_time
            data["date_time"] = (
                data["Date"].astype(str) + " " + data["Time"].astype(str)
            )

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

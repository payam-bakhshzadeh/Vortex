import pandas as pd


class DataProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.file_path = None
        self.mode = "new_only"

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_mode(self, mode):
        self.mode = mode

    def check_duplicates(self, file_path):
        new_data = pd.read_csv(file_path)
        existing_data = self.db_manager.get_market_data()

        if "Date" in new_data.columns and "Time" in new_data.columns:
            new_data["datetime"] = pd.to_datetime(
                new_data["Date"] + " " + new_data["Time"]
            )
        elif "Date" in new_data.columns:
            new_data["datetime"] = pd.to_datetime(new_data["Date"])

        if existing_data.empty:
            return False

        if "datetime" not in existing_data.columns:
            return False

        return not new_data["datetime"].isin(existing_data["datetime"]).empty

    def process_and_save(self, datetime_col="datetime"):
        if not self.file_path:
            raise ValueError("No file selected")

        new_data = pd.read_csv(self.file_path)

        if "Date" in new_data.columns and "Time" in new_data.columns:
            new_data[datetime_col] = pd.to_datetime(
                new_data["Date"] + " " + new_data["Time"]
            )
            new_data.drop(["Date", "Time"], axis=1, inplace=True)
        elif "Date" in new_data.columns:
            new_data[datetime_col] = pd.to_datetime(new_data["Date"])
            new_data.drop(["Date"], axis=1, inplace=True)

        if self.mode == "replace":
            self.db_manager.store_market_data(new_data)
        else:
            existing_data = self.db_manager.get_market_data()
            if not existing_data.empty:
                new_data = new_data[
                    ~new_data[datetime_col].isin(existing_data[datetime_col])
                ]
            self.db_manager.append_market_data(new_data)

import json
from pathlib import Path


class FileHandler:
    def __init__(self, default_path="output.json"):
        self.default_path = self.ensure_json_extension(default_path)
        self.current_path = self.load_last_path()

    def ensure_json_extension(self, path):
        """Ensure the file has a .json extension."""
        if not path.endswith(".json"):
            path += ".json"
        return path

    def load_last_path(self):
        """Load the last saved path from a configuration file."""
        config_path = Path("config.json")
        if config_path.exists():
            with config_path.open('r') as f:
                config = json.load(f)
                return config.get("json_save_path", self.default_path)
        return self.default_path

    def save_last_path(self, path):
        """Save the current path to a configuration file."""
        config_path = Path("config.json")
        config = {}
        if config_path.exists():
            with config_path.open('r') as f:
                config = json.load(f)
        config["json_save_path"] = path
        with config_path.open('w') as f:
            json.dump(config, f, indent=4)

    def write_json(self, data, directory=None):
        """Write data to a JSON file in the specified directory."""
        if directory is None:
            directory = self.current_path
        else:
            self.current_path = directory
            self.save_last_path(directory)

        directory_path = Path(directory)
        if not directory_path.exists() or not directory_path.is_dir():
            # Use current working directory if the specified directory is invalid
            directory_path = Path.cwd()

        file_path = directory_path / "MT4.json"
        with file_path.open('w') as f:
            json.dump(data, f, indent=4)
        return str(file_path)

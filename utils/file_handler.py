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
                return self.ensure_json_extension(config.get("json_save_path", self.default_path))
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

    def write_json(self, data, path=None):
        """Write data to a JSON file."""
        if path is None:
            path = self.current_path
        else:
            path = self.ensure_json_extension(path)
            self.current_path = path
            self.save_last_path(path)
        with Path(path).open('w') as f:
            json.dump(data, f, indent=4)
        return path

import json
import os


class ConfigLoader:
    def __init__(self, config_path: str):
        """
        Initialize the ConfigLoader with the path to the JSON configuration file.
        """
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        """
        Load and parse the JSON configuration file.
        Returns the parsed data as a dictionary.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON file: {e}")

        return data

    def get(self, key: str, default=None):
        """
        Retrieve a value from the configuration data using the provided key.
        If the key doesn't exist, return the default value.
        """
        return self.config_data.get(key, default)

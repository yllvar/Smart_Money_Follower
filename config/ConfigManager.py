import argparse
import yaml
from yaml import YAMLError
import os


class ConfigManager:
    def __init__(self, args=None):
        self._config_path = os.path.abspath(args.config)
        self._config_data = self._load_config()
        self._args = args
        self._final_config = self._merge_config_and_args()

    def _load_config(self):
        """Load the configuration file."""
        try:
            with open(self._config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file '{self._config_path}' not found. Using defaults.")
            return {}
        except YAMLError as e:
            print(f"Error: Failed to parse YAML in config file '{self._config_path}': {e}")
            return {}

    def _merge_config_and_args(self):
        """Merge the config file and command-line arguments, with args taking precedence."""
        wallet_settings = self._config_data.get("wallet_settings", {})
        return {
            "path": self._args.path if self._args and self._args.path else self._config_data.get("path", "data"),
            "verbose": self._args.verbose if self._args and self._args.verbose else self._config_data.get("verbose", True),
            "export_format": self._args.export_format if self._args and self._args.export_format else self._config_data.get("export_format", "csv"),
            "timeframe": wallet_settings.get("timeframe", "7d"),
            "wallet_tag": wallet_settings.get("wallet_tag", "smart_degen")
        }

    def validate(self):
        """Validate the final configuration."""
        if not self._final_config["path"]:
            raise ValueError("Export path is required.")
        if self._final_config["export_format"] not in ["csv", "txt"]:
            raise ValueError(f"Unsupported export format: {self._final_config['export_format']}")

    @property
    def path(self):
        return self._final_config["path"]

    @path.setter
    def path(self, new_path):
        if not isinstance(new_path, str):
            raise ValueError("Path must be a string.")
        self._final_config["path"] = new_path

    @property
    def verbose(self):
        return self._final_config["verbose"]

    @verbose.setter
    def verbose(self, verbose):
        if not isinstance(verbose, bool):
            raise ValueError("Verbose must be a boolean.")
        self._final_config["verbose"] = verbose

    @property
    def export_format(self):
        return self._final_config["export_format"]

    @export_format.setter
    def export_format(self, export_format):
        if export_format not in ["csv", "txt"]:
            raise ValueError("Export format must be 'csv' or 'txt'")
        self._final_config["export_format"] = export_format

    @property
    def timeframe(self):
        return self._final_config["timeframe"]

    @timeframe.setter
    def timeframe(self, timeframe):
        if timeframe not in ["1d", "7d", "30d"]:
            raise ValueError("Timeframe must be 1d, 7d, 30d")
        self._final_config["timeframe"] = timeframe

    @property
    def wallet_tag(self):
        return self._final_config["wallet_tag"]

    @wallet_tag.setter
    def wallet_tag(self, wallet_tag):
        tag_options = ["all", "pump_smart", "smart_degen", "reowned", "snipe_bot"]
        if wallet_tag not in tag_options:
            raise ValueError("Wallet Tag must be set to a valid tag")
        self._final_config["wallet_tag"] = wallet_tag

    @property
    def config(self):
        return self._final_config


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Smart Money Follower Configuration")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to the config file")
    parser.add_argument("--path", type=str, help="Path to export files")
    parser.add_argument("--verbose", type=bool, help="Verbose script logs")
    parser.add_argument("--export-format", type=str, choices=["csv", "txt"], help="Export format (csv or txt)")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse arguments
    args = parse_args()
    args.config = "config.yaml" # for testing purposes

    # Create ConfigManager instance
    config_manager = ConfigManager(args=args)

    # Validate the configuration
    try:
        config_manager.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)

    # Access properties
    print("Final Configuration:")
    print(f"Path: {config_manager.path}")
    print(f"Verbose: {config_manager.verbose}")
    print(f"Export Format: {config_manager.export_format}")
    print(f"Timeframe: {config_manager.timeframe}")
    print(f"Wallet Tag: {config_manager.wallet_tag}")
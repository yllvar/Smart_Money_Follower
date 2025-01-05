import argparse
import yaml
import os
from yaml import YAMLError
from config_validators import *


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
            "path": validate_path(
                self._args.path if self._args and self._args.path else self._config_data.get("path", "data")
            ),
            "verbose": validate_verbose(
                self._args.verbose if self._args and self._args.verbose else self._config_data.get("verbose", True)
            ),
            "export_format": validate_export_format(
                self._args.export_format if self._args and self._args.export_format else self._config_data.get("export_format", "csv")
            ),
            "timeframe": validate_timeframe(
                wallet_settings.get("timeframe", "7d"),
            ),
            "wallet_tag": validate_wallet_tag(
                wallet_settings.get("wallet_tag", "smart_degen")
            ),
            "win_rate": validate_win_rate(
                wallet_settings.get("win_rate", 60)
            )
        }

    @property
    def path(self):
        return self._final_config["path"]

    @path.setter
    def path(self, new_path):
        self._final_config["path"] = validate_path(new_path)

    @property
    def verbose(self):
        return self._final_config["verbose"]

    @verbose.setter
    def verbose(self, verbose):
        self._final_config["verbose"] = validate_verbose(verbose)

    @property
    def export_format(self):
        return self._final_config["export_format"]

    @export_format.setter
    def export_format(self, export_format):
        self._final_config["export_format"] = validate_export_format(export_format)

    @property
    def timeframe(self):
        return self._final_config["timeframe"]

    @timeframe.setter
    def timeframe(self, timeframe):
        self._final_config["timeframe"] = validate_timeframe(timeframe)

    @property
    def wallet_tag(self):
        return self._final_config["wallet_tag"]

    @wallet_tag.setter
    def wallet_tag(self, wallet_tag):
        self._final_config["wallet_tag"] = validate_wallet_tag(wallet_tag)

    @property
    def win_rate(self):
        return self._final_config["win_rate"]

    @win_rate.setter
    def win_rate(self, win_rate):
        self._final_config["win_rate"] = validate_win_rate(win_rate)

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
    parser.add_argument("--winrate", type=int, help="Set winrate between 0 and 100")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse arguments
    args = parse_args()
    args.config = "config.yaml" # for testing purposes

    # Create ConfigManager instance
    config_manager = ConfigManager(args=args)

    # Access properties
    print("Final Configuration:")
    print(f"Path: {config_manager.path}")
    print(f"Verbose: {config_manager.verbose}")
    print(f"Export Format: {config_manager.export_format}")
    print(f"Timeframe: {config_manager.timeframe}")
    print(f"Wallet Tag: {config_manager.wallet_tag}")
    print(f"Win Rate: {config_manager.win_rate}")
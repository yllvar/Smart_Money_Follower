import argparse
import json
from json import JSONDecodeError
from datetime import datetime


def load_config(file_path):
    """Load the configuration file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: config file '{file_path}' not found. Using defaults")
        return {}
    except JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in config file '{file_path}': {e}")
        return {}



def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Smart Money Follower Configuration")
    parser.add_argument("--config", type=str, default="./config/config.json", help="Path to the config file")
    parser.add_argument("--path", type=str, default="./data", help="Path to Export")
    parser.add_argument("--log-level", type=str, help="Logging level (e.g., DEBUG, INFO)")
    parser.add_argument("--export-format", type=str, choices=["csv", "txt"], default="csv",
                        help="Format for exporting data (csv or txt)")
    return parser.parse_args()


def merge_config_and_args(config, args):
    """Merge the config file and command-line arguments, with args taking precedence."""
    return {
        "config": args.config,
        "path": args.path,
        "log_level": args.log_level or config.get("log_level", "INFO"),  # Default to INFO
        "export_format": args.export_format or config.get("export_format", "csv")  # Default to csv
    }


if __name__ == "__main__":
    # Parse arguments
    args = parse_args()

    # Load the config file
    config = load_config(args.config)

    # Merge configurations
    final_config = merge_config_and_args(config, args)

    # Validate final configuration
    if not final_config["path"]:
        print("Error: Export path is required.")
        exit(1)

    if final_config["export_format"] not in ["csv", "txt"]:
        print(f"Error: Unsupported export format '{final_config['export_format']}'")
        exit(1)

    # Print final configuration
    print("Final Configuration:")
    for key, value in final_config.items():
        print(f"{key}: {value}")

import argparse
import yaml
from yaml import YAMLError
import os

def load_config(file_path):
    """Load the configuration file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Config file '{file_path}' not found. Using defaults.")
        return {}
    except YAMLError as e:
        print(f"Error: Failed to parse YAML in config file '{file_path}': {e}")
        return {}


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Smart Money Follower Configuration")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to the config file")
    parser.add_argument("--path", type=str, help="Path to export files")
    parser.add_argument("--verbose", type=str, help="Verbose script logs")
    parser.add_argument("--export-format", type=str, choices=["csv", "txt"], help="Export format (csv or txt)")
    return parser.parse_args()


def merge_config_and_args(config, args):
    """Merge the config file and command-line arguments, with args taking precedence."""
    return {
        "path": args.path or config.get("path", "data"),
        "verbose": args.verbose or config.get("verbose", True),
        "export_format": args.export_format or config.get("export_format", "csv"),
    }

def get_final_config(args):
    """Main entry point for obtaining the final configuration."""
    # Load the config file
    config_path = os.path.abspath(args.config)
    config_data = load_config(config_path)

    # Merge configurations
    final_config = merge_config_and_args(config_data, args)

    # Validate final configuration
    if not final_config["path"]:
        raise ValueError("Export path is required.")
    if final_config["export_format"] not in ["csv", "txt"]:
        raise ValueError(f"Unsupported export format: {final_config['export_format']}")

    return final_config


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

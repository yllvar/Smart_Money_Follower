def validate_path(path):
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    return path

def validate_verbose(verbose):
    if not isinstance(verbose, bool):
        raise ValueError("Verbose must be a boolean")
    return verbose

def validate_export_format(export_format):
    valid_formats = ["csv", "txt"]
    if export_format not in valid_formats:
        raise ValueError("Export format must be 'csv' or 'txt'")
    return export_format

def validate_timeframe(timeframe):
    valid_timeframes = ["1d", "7d", "30d"]
    if timeframe not in valid_timeframes:
        raise ValueError("Timeframe must be '1d', '7d', or '30d'.")
    return timeframe

def validate_wallet_tag(wallet_tag):
    valid_tags = ["all", "pump_smart", "smart_degen", "reowned", "snipe_bot"]
    if wallet_tag not in valid_tags:
        raise ValueError(f"Wallet tag must be one of {valid_tags}")
    return wallet_tag

def validate_win_rate(win_rate):
    if not isinstance(win_rate, int):
        raise ValueError("Win Rate must be an integer")
    elif not (0 <= win_rate <= 100):
        raise ValueError("Win Rate must be between 0 and 100")
    return win_rate / 100
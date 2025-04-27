import os
import json
from pathlib import Path
from stock_analysis.stock_analyzer import analyze_stock

# Load the config file
base_path = Path(__file__).resolve().parents[2]  # Go up to TradeLenseNepse/
config_path = base_path / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)

def analyze_stock_for_notebook(stock_shortname):
    """
    Look up the full CSV file path from the config file and analyze the stock.
    """
    if stock_shortname not in config["csv_files"]:
        raise ValueError(f"{stock_shortname} not found in config.json.")
    
    csv_path = config["csv_files"][stock_shortname]

    # Debugging: Print the full path to verify it
    print("Attempting to read file:", csv_path)
    
    analyze_stock(csv_path)

    
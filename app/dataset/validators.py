import os

def validate_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError("CSV file not found on your machine")

    if not path.lower().endswith(".csv"):
        raise ValueError("Only CSV files are allowed")

    return True
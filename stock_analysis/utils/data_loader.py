import pandas as pd  # Import pandas for data handling

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data from {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the file: {e}")

def preprocess_data(df):
    """
    Perform basic preprocessing on the DataFrame.
    - Converts 'Date' column to datetime.
    - Sorts the data by date.
    """
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values('Date', inplace=True)
        except Exception as e:
            raise ValueError(f"Error while preprocessing the 'Date' column: {e}")
    else:
        raise ValueError("The DataFrame does not contain a 'Date' column.")
    return df

def load_and_preprocess_csv(file_path):
    """
    Load and preprocess a CSV file.
    Combines `load_csv` and `preprocess_data`.
    """
    df = load_csv(file_path)
    df = preprocess_data(df)
    return df
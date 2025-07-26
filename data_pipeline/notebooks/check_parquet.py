def main():
    import os
    import sys
    import pandas as pd

    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python check_parquet.py <path_to_parquet_file>")
        sys.exit(1)

    parquet_file_path = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(parquet_file_path):
        print(f"File not found: {parquet_file_path}")
        sys.exit(1)

    # Read the Parquet file
    try:
        df = pd.read_parquet(parquet_file_path)
        print("Parquet file loaded successfully.")
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        sys.exit(1)
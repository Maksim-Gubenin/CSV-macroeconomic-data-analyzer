"""
Utility module for reading data from multiple CSV files.
"""
import csv
import os


def read_csv_files(file_paths: list) -> list[dict]:
    """
    Reads data from multiple CSV files and combines them into a single list of dictionaries.

    Args:
        file_paths: A list of paths to the CSV files to read.

    Returns:
        A list of dictionaries, where each dictionary represents a row from the CSV files.

    Raises:
        FileNotFoundError: If any of the specified files do not exist.
    """
    all_data = []

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не существует")

        with open(file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                all_data.append(row)

    return all_data

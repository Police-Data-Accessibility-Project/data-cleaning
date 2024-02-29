"""
This is the main pipeline for data processing.
This pipeline will take a csv of duplicate entries and
attempt to resolve them by finding possible correct urls.
That data will then be ingested by the Flask app for review.
"""
import argparse
import polars as pl
from Deduplicator import Deduplicator
from data_processing.DatabaseManager import DatabaseManager


def load_csv(file_path: str = "input.csv") -> pl.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data.
    """
    return pl.read_csv(file_path)

def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--csv', type=str, help='The path to the CSV file.')
    parser.add_argument('--airtable', type=bool, default=False, help='Whether to load data from Airtable.')
    return parser.parse_args()

if __name__ == "__main__":

    deduplicator = Deduplicator()
    deduplicator.find_possible_correct_urls()




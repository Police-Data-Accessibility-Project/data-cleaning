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
    # Parse command line arguments on whether to load data from csv or airtable
    args = parse_args()

    # Load data from either csv or airtable
    if args.csv:
        data = load_csv(args.csv)
    elif args.airtable:
        deduplicator = Deduplicator()
        data = deduplicator.get_agency_data()
    else:
        raise ValueError("Either --csv or --airtable must be provided.")

    # Identify duplicates
    deduplicator = Deduplicator()
    duplicates = deduplicator.identify_duplicates(data)

    # Find possible correct urls
    proposed_correct_url_entries = deduplicator.find_possible_correct_urls(duplicates)

    # Load data into data_correction.db
    dm = DatabaseManager()
    dm.create_table()
    dm.insert_entries(proposed_correct_url_entries)
    dm.close()



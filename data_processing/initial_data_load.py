from data_processing.DatabaseManager import DatabaseManager
from data_processing.Deduplicator import Deduplicator
from data_processing.pipeline import parse_args, load_csv

"""
This script will load the initial data, 
either directly form airtable or from a csv file,
and then identify duplicates and load them into the database.
"""

if __name__ == '__main__':
    # Parse command line arguments on whether to load data from csv or airtable
    args = parse_args()

    # Load data from either csv or airtable
    if args.csv:
        data = load_csv(args.csv)
    elif args.airtable:
        deduplicator = Deduplicator()  # TODO: Change so that agency data isn't pulled from duplicator
        data = deduplicator.get_agency_data()
    else:
        raise ValueError("Either --csv or --airtable must be provided.")

    # Validate that data has correct columns
    columns = ['name', 'state_iso', 'url', 'homepage_url']

    dm = DatabaseManager()
    # Truncate database table
    dm.reset_database()

    # Identify duplicates, in format of url -> list of entries
    deduplicator = Deduplicator()
    duplicates = deduplicator.identify_duplicates(data)

    # Convert duplicates to list of entries
    data = []
    for key, value in duplicates.items():
        for item in value:
            entry = {
                'name': item['name'],
                'state': item['state_iso'],
                'old_url': key,
                'possible_correct_url': '',
                'airtable_uid': item['airtable_uid'],
                'submitted_name': item['submitted_name'],
                'no_web_presence': item['no_web_presence'],
                'rejection_reason': '',
                'approved': ''
            }
            data.append(entry)

    # Create database and load data into it
    dm.create_table()
    dm.insert_initial_data(data)



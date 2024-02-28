from typing import List, Dict

import polars as pl
import pandas as pd

from GoogleSearcher import GoogleSearcher
from data_processing.DatabaseManager import DatabaseManager


class Deduplicator:

    """
    Identifies and then attempts to resolve duplicates
    """
    def __init__(self):
        self.google_searcher = GoogleSearcher()


    def get_agency_data(self) -> pl.DataFrame:
        """
        Retrieves agency data from airtable database

        Returns:
            pl.DataFrame: agency data
        """


    def find_possible_correct_urls(self):
        """
        Finds possible correct urls for duplicates, utilizing the Google custom Search JSON API to
        attempt to find home pages based on the information in the duplicates

        Args:
            duplicates (dict): duplicates

        Returns:
            dict: dictionary of possible correct urls
        """
        dm = DatabaseManager()
        entries = dm.get_entries_without_proposed_url()
        for url, duplicate_list in entries.items():
            for entry in duplicate_list:
                state = entry['state']
                name = entry['name']
                search_string = f'{name} {state} Home Page'
                # search for possible correct url
                try:
                    search_results = self.google_searcher.search(search_string)
                except Exception as e:
                    # If exception mentions quota, stop search
                    if "Quota" in str(e):
                        print("Quota exceeded for the day")
                        return proposed_correct_url_entries
                    else:
                        raise e
                # For now, select only first search result as possible correct url
                possible_correct_url = search_results[0]['link']
                proposed_correct_url_entry = {
                    'name': name,
                    'state': state,
                    'old_url': url,
                    'possible_correct_url': possible_correct_url
                }
                proposed_correct_url_entries.append(proposed_correct_url_entry)

        return proposed_correct_url_entries



    def identify_duplicates(self, agency_data: pl.DataFrame) -> dict[str, list[dict, str]]:
        """
        Identifies duplicates in agency data
        Duplicates are turned in the structure of
         a dictionary with the key being the duplicate url
         and the value being a list of duplicates

        Args:
            agency_data (dict): agency data

        Returns:
            list: list of duplicates
        """
        # Create a dictionary to store duplicates
        duplicates: dict[str, list[dict, str]] = {}
        # Create a dictionary to store urls
        urls: dict[str, list[dict, str]] = {}

        # Iterate through the agency data
        for index, row in agency_data.to_pandas().iterrows():
            url = row['homepage_url']
            # If the url is not in the urls dictionary, add it
            if url not in urls:
                urls[url] = []
            # Add the row to the urls dictionary
            urls[url].append(row)

        # Iterate through the urls dictionary
        for url, url_list in urls.items():
            # If the length of the url list is greater than 1, add it to the duplicates dictionary
            if len(url_list) > 1:
                duplicates[url] = url_list

        return duplicates


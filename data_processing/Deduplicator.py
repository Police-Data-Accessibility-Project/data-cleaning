from typing import List, Dict

import polars as pl
import pandas as pd

from GoogleSearcher import GoogleSearcher
from data_processing.DatabaseManager import DatabaseManager

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


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
        for entry in entries:
            state = states[entry['state']]
            name = entry['name']
            # search for possible correct url
            try:
                search_results = self.google_searcher.search(
                    query=f'{name} {state} Home Page'
                )
            except Exception as e:
                # If exception mentions quota, stop search
                if "Quota" in str(e):
                    print("Quota exceeded for the day. Original error: ", e)
                    return
                else:
                    raise e
            # For now, select only first search result as possible correct url
            # Log
            possible_correct_url = search_results[0]['link']
            print(f"Found {possible_correct_url} results for {name} {state} Home Page")
            dm.update_entry(entry['id'], possible_correct_url)


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


"""
Fun fact: This can be read as both "PDAP Interface" or "PDAP API Interface"
"""
import os
import requests
import polars as pl
import itertools
from dotenv import load_dotenv


class PDAPInteface:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("PDAP_API_KEY")
        self.base_url = "https://data-sources.pdap.io"

    def get_agency_data(self) -> pl.DataFrame:
        raise NotImplementedError("This method depends on the PDAP API which is not yet implemented")
        responses = []
        counter = itertools.count(start=1)
        while True:
            page = next(counter)
            response = requests.get(
                url=f"{self.base_url}/agencies/{page}",
                headers={
                "Authorization": f"Bearer {self.api_key}"
            })
            if response.status_code != 200:
                break
            responses.append(response.json())

if __name__ == "__main__":
    pdap = PDAPInteface()
    data = pdap.get_agency_data()
    print(data)
    print(data.shape)
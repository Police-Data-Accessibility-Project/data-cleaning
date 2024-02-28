from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

class GoogleSearcher:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("CUSTOM_SEARCH_API_KEY")
        self.cse_id = os.getenv("CUSTOM_SEARCH_ID")
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def search(self, query: str) -> list[dict]:

        try:
            res = self.service.cse().list(q=query, cx=self.cse_id).execute()
            return res['items']
            # Process your results
        except HttpError as e:
            if e.resp.status == 403:
                raise HttpError(f"Quota exceeded for the day. Original Error: {e}")
            else:
                raise HttpError(f"An error occurred: {e}")

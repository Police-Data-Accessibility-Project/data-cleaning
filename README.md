This is a browser-based tool used to assist in resolving duplicate urls in the PDAP Agencies Airtable.

Pulls data from [PDAP Agencies Airtable](https://airtable.com/app473MWXVJVaD7Es/shr43ihbyM8DDkKx4/tblpnd3ei5SlibcCX).

Before running, make sure to install the required packages.

```bash
pip install -r requirements.txt
```

To utilize this tool, either utilize the PDAP Interface (not currently completed) or download a csv of the Agencies data and run initial_data_load.py to load the data into the database.

```bash
python data_processing/initial_data_load.py --csv input.csv
```

And then run pipeline.py to pull data from the web and update the database.

```bash
python data_processing/pipeline.py
```

Finally, run the following command to start up the web server.

```bash
python app/app.py
```

When finished reviewing, run export.py

```base
python data_processing/export.py
```

The end result should exist as 'export.csv' in the root directory. 

### ENVIRONMENT VARIABLES
To run pipeline.py, you will need to set the following environment variables:

- CUSTOM_SEARCH_API_KEY (Google Custom Search API Key)
- CUSTOM_SEARCH_ENGINE_ID (Google Custom Search Engine ID)

To obtain these variables, follow the instructions in [Google's Custom Search API documentation](https://developers.google.com/custom-search/v1/overview).

Note that if you are using a free tier, you will only be able to obtain at most 100 proposed urls per day.
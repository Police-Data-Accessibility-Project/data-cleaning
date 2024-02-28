from data_processing.GoogleSearcher import GoogleSearcher

def test_search():
    # Instantiate the GoogleSearcher class
    google_searcher = GoogleSearcher()

    original_url = "https://www.yorkville.il.us/212/Police-Department"
    # Define an arbitrary query
    query1 = "Yorkville Police Department - Illinois"
    query2 = "Yorkville Police Department - New York"

    # Define an arbitrary query
    # Call the search method with the query
    print(f"Original URL: {original_url}")
    for query in (query1, query2):
        query = f"{query} Department Home Page"
        print("Query:", query)
        results = google_searcher.search(query)
        result = results[0]
        print(f"{result['title']} - {result['link']} - {result['snippet']}")
        print("=" * 100)



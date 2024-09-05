import json
from bs4 import BeautifulSoup

def extract_search_results(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the <search> element
    search_element = soup.find('search')
    
    # Get the JSON string from the :search-result-default attribute
    json_string = search_element.get(':search-result-default')
    
    # Parse the JSON string
    search_results = json.loads(json_string)
    
    return search_results


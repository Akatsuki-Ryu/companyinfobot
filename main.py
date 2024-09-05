from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time
from extract_search_results import extract_search_results
app = Flask(__name__)

def search_company(company_name):
    url = f"https://www.allabolag.se/what/{company_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all(class_="search-results")
    return str(results[0]) if results else "No results found"

def extract_orgnr_from_results(results):
    soup = BeautifulSoup(results, 'html.parser')
    orgnrs = []
    for result in soup.find_all('search'):
        orgnr = result.get('orgnr')
        if orgnr:
            orgnrs.append(orgnr)
    return orgnrs

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        company_list = request.form['company_list'].split('\n')
        for company in company_list:
            raw_search_results = search_company(company)
            search_results = extract_search_results(raw_search_results)
            print(search_results)
            # if search_results != "No results found":
                # orgnrs = extract_orgnr_from_results(raw_search_results)
                # results.append({"company": company, "orgnrs": orgnrs})
            # else:
                # results.append({"company": company, "orgnrs": ["Not found"]})
            time.sleep(2)  # Add a 2-second delay between requests
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
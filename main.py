import json
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
            #clean the results list for the next iteration
        results = []
        company_list = request.form['company_list'].split('\n')
        # if the company list is too long, more than 10 companies, ask the user to enter only 10 companies at a time
        if len(company_list) > 10:
            return render_template('index.html', results=results, error="Please enter only 10 companies at a time")
        for company in company_list:
            raw_search_results = search_company(company)
            search_results = extract_search_results(raw_search_results)
            
            # Write search results to a file in the scrapedata folder and beautify it
            import os
            
            # Create the scrapedata folder if it doesn't exist
            os.makedirs('scrapedata', exist_ok=True)
            
            # Write the file to the scrapedata folder
            with open(os.path.join('scrapedata', f"{company}_search_results.json"), "w", encoding="utf-8") as f:
                json.dump(search_results, f, ensure_ascii=False, indent=4)

            
            
            if search_results:
                orgnr = search_results[0].get('orgnr', 'Not found')
                real_company_name = search_results[0].get('jurnamn', 'Not found')
                industry = search_results[0].get('abv_hgrupp', 'Not found')
                if company != real_company_name:
                    results.append({"remarks": "company name mismatch", "company": company, "real_company_name": real_company_name, "orgnrs": [orgnr], "industry": industry})
                else:
                    results.append({"company": company, "orgnrs": [orgnr], "industry": industry})
            else:
                results.append({"company": company, "orgnrs": ["Not found"], "industry": "Not found"})
            
            # Original code for future use
            # if search_results:
            #     orgnrs = [result.get('orgnr', 'Not found') for result in search_results]
            #     results.append({"company": company, "orgnrs": orgnrs})
            # else:
            #     results.append({"company": company, "orgnrs": ["Not found"]})
            print(search_results)
            time.sleep(0.5) #anti spamming measure
            
            # if search_results != "No results found":
                # orgnrs = extract_orgnr_from_results(raw_search_results)
                # results.append({"company": company, "orgnrs": orgnrs})
            # else:
                # results.append({"company": company, "orgnrs": ["Not found"]})

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
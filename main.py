from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def search_company(company_name):
    url = f"https://www.allabolag.se/what/{company_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all(class_="search-results")
    # save the results to a file as an example 
    with open('sample_results.txt', 'w') as f:
        f.write(str(results[0]))
    return results[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_list = request.form['company_list'].split('\n')
        results = []
        for company in company_list:
            search_results = search_company(company)
            print(search_results)
            if search_results:
                results.append(f"{company}: {search_results}")
            else:
                results.append(f"{company}: Not found")
            time.sleep(2)  # Add a 2-second delay between requests
        return jsonify(results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
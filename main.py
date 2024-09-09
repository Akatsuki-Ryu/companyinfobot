import json
from flask import Flask, render_template, request, send_file, jsonify
import requests
from bs4 import BeautifulSoup
import time
from extract_search_results import extract_search_results
import os

from fomulateurl import formulate_url
app = Flask(__name__)

def search_company(company_name):
    #preprocess the company name to remove special characters and spaces, and make it lowercase,replace the space with %20
    company_name = company_name.replace(" ", "%20") 
    company_name = company_name.replace("ä", "a")
    company_name = company_name.replace("ö", "o")
    company_name = company_name.replace("å", "a")
    company_name = company_name.replace("é", "e")
    company_name = company_name.replace("á", "a")
    company_name = company_name.replace("í", "i")
    company_name = company_name.replace("ó", "o")
    company_name = company_name.replace("ú", "u")
    company_name = company_name.replace("ü", "u")
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

progress = 0
total = 0
query_process_flag = False

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    global progress 
    global total
    if request.method == 'POST':
        #start the query process
        global query_process_flag
        query_process_flag = True
        company_list = request.form.get('company_list', '').split('\n')
        company_list = [company.strip() for company in company_list if company.strip()]
        
        if not company_list:
            query_process_flag = False
            return render_template('index.html', results=results, error="Please enter at least one company name.")
        
        if len(company_list) > 100:
            query_process_flag = False
            return render_template('index.html', results=results, error="Please enter only 100 companies at a time")
        
        #make a progress bar

        total = len(company_list)
        progress = 0
        
        for company in company_list:
            if not query_process_flag:
                #if the query process is terminated, break the loop
                break

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
                #only get the first result from the search results
                orgnr = search_results[0].get('orgnr', 'Not found')
                real_company_name = search_results[0].get('jurnamn', 'Not found')
                industry = search_results[0].get('abv_hgrupp', 'Not found')
                url = formulate_url(orgnr)
                if company != real_company_name:
                    results.append({"remarks": "check company name", "company": company, "real_company_name": real_company_name, "orgnrs": [orgnr], "industry": industry, "url": url})
                else:
                    results.append({"remarks": "", "company": company,"real_company_name": real_company_name, "orgnrs": [orgnr], "industry": industry, "url": url})
                #write the results to a csv file, appending the results to the csv file
                import csv
                import os

                # Create the resultsdata folder if it doesn't exist
                os.makedirs('resultsdata', exist_ok=True)

                csv_path = os.path.join('resultsdata', 'results.csv')
                with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # if the file is empty, write the header
                    if f.tell() == 0:
                        writer.writerow(["Query Company Name", "Real Company Name", "Organization Number", "Industry", "URL", "Remarks"])
                    for result in results:
                        writer.writerow([result["company"], result["real_company_name"], result["orgnrs"][0], result["industry"], result["url"], result.get("remarks", "")])
            else:
                results.append({"company": company, "orgnrs": ["Not found"], "industry": "Not found"})
            
            # Original code for future use
            # if search_results:
            #     orgnrs = [result.get('orgnr', 'Not found') for result in search_results]
            #     results.append({"company": company, "orgnrs": orgnrs})
            # else:
            #     results.append({"company": company, "orgnrs": ["Not found"]})
            print(search_results)
            progress += 1
            time.sleep(0.5) #anti spamming measure

            
            # if search_results != "No results found":
                # orgnrs = extract_orgnr_from_results(raw_search_results)
                # results.append({"company": company, "orgnrs": orgnrs})
            # else:
                # results.append({"company": company, "orgnrs": ["Not found"]})
        query_process_flag = False
        time.sleep(2)
    return render_template('index.html', results=results, total=total)

@app.route('/download_csv')
def download_csv():
    csv_path = 'resultsdata/results.csv'
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True, download_name='company_orgnr_results.csv')
    else:
        return "No results available for download", 404

@app.route('/clear_csv', methods=['POST'])
def clear_csv():
    csv_path = 'resultsdata/results.csv'
    try:
        if os.path.exists(csv_path):
            os.remove(csv_path)
            return "CSV file cleared successfully", 200
        else:
            return "No CSV file found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/get_progress', methods=['GET'])
def get_progress():
    global progress
    global total
    return jsonify({"progress": progress, "total": total})

@app.route('/get_query_process_flag', methods=['GET'])
def get_query_process_flag():
    global query_process_flag
    return jsonify({"query_process_flag": query_process_flag})

@app.route('/terminate', methods=['GET'])
def terminate():
    global query_process_flag
    query_process_flag = False
    return "Backend Query process terminated", 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
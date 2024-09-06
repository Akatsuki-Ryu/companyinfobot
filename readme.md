# Company Org Number Finder

This is a web application powered by Python and Flask that allows users to find organization numbers for companies in Sweden. Here's what the application does:

1. Provides a web interface where users can input a list of company names.
2. For each company, it searches for information on https://www.allabolag.se/.
   - The search query is formulated as: https://www.allabolag.se/what/{companyname}
3. From the search results, it extracts the following information:
   - Organization number (Org.nummer)
   - Real company name
   - Industry
4. The application handles potential mismatches between input company names and real company names.
5. Results are displayed on the web page and also saved to a CSV file.
6. Users can download the CSV file with all results.
7. Users have the option to clear the CSV file.

Key Features:
- Web-based interface for easy input and result viewing
- Handles multiple companies (up to 10 at a time)
- Saves results to a CSV file for easy data management
- Download option for the CSV file
- Clear CSV function to start fresh
- Error handling for empty inputs or too many companies
- Anti-spam measures to prevent overloading the search website

Note: This application uses web scraping techniques to gather information. Please ensure you comply with the terms of service of https://www.allabolag.se/ when using this application.

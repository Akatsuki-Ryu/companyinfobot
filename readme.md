this is an AI powered project written in python to do the following:

1. load a company list from a txt file
2. for each company, search this company's info in this website: https://www.allabolag.se/
    2.1 to find the company, we need to formulate the search query, for example: https://www.allabolag.se/what/{companyname}
3. in the search result, find the company's org number (Org.nummer)
    3.1 send the result to AI to extract the org number, i have a lm-studio running on my local computer, so i can use the API to send the result to the LM-studio for extraction
    3.2 there might be several search results, we need to find the one that is the most relevant to the company name
4. write back the company's org number to the txt file beside the company name
5. save the txt file

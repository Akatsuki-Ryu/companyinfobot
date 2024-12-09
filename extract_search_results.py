import json
# the input will be like this [{'mainOffice': None, 'name': 'HONDA ACCESS EUROPE NV', 'orgnr': '5020590237', 'businessUnitId': None, 'companyId': '2B14O7XI5YCRG', 'listingId': '2B14O7XI5YCRG', 'customerId': '5020590237', 'phone': '0406412700', 'phone2': None, 'mobile': '0406412700', 'mobile2': None, 'faxNumber': None, 'homePage': None, 'email': None, 'marketingProtection': False, 'industries': [{'code': '10000924', 'name': 'Agenturer', 'description': None, 'style': None, 'companyId': '2B14O7XI5YCRG', 'salesRank': None}, {'code': '10001228', 'name': 'Bilar', 'description': None, 'style': None, 'companyId': '2B14O7XI5YCZW', 'salesRank': None}, {'code': '10001335', 'name': 'Bilreservdelar', 'description': None, 'style': None, 'companyId': '2B14O7XI5YD2V', 'salesRank': None}], 'location': None, 'currentIndustry': {'code': '10000924', 'name': 'Agenturer', 'description': None, 'companyId': None}, 'visitorAddress': None, 'postalAddress': None, 'description': None, 'advertType': None, 'logo': None, 'searchResultImage': None, 'legalName': 'HONDA ACCESS EUROPE NV', 'revenue': None, 'currency': None, 'profit': None, 'companyAccountsLastUpdatedDate': None, 'employees': '0', 'contactPerson': None, 'status': None, 'statusRemarks': [], 'certificates': [], 'rating': None, 'ratingSettings': None}]
def extract_orgnr_from_results(results):
    data = json.loads(results)
    if data:
        orgnr = data.get('orgnr')
        if orgnr:
            return format_orgnr(orgnr)
        

    


def format_orgnr(orgnr):
    # the input would be like this 5020590237, make it like this 502059-0237
    orgnr = f"{orgnr[:6]}-{orgnr[6:]}"
    return orgnr


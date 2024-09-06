#given the orgnr, formulate the url to get the company info
def formulate_url(orgnr):
    #take the hiphen and remove it
    orgnr = orgnr.replace("-", "")
    return f"https://www.allabolag.se/{orgnr}"

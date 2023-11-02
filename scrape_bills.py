import requests
from bs4 import BeautifulSoup
import json

#Prepare JSON file to which to write results
resultsfile = open("results.json", 'w')

URL = "https://mgaleg.maryland.gov/mgawebsite/Members/Details/wu01"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
billTable = soup.find(id="billIndexMobile")

#Obtain a list of house bills sponsored by Delegate Wu
sponsoredBills = {}
for link in billTable.find_all("a"):
    linkText = str(link.text)
    if (linkText[0] == "H"):
        sponsoredBills[linkText] = [""]

#Obtain the list of sponsors for each bill
for bill in sponsoredBills:
    page = requests.get("https://mgaleg.maryland.gov/mgawebsite/Legislation/Details/" + bill.lower() + "?ys=2023RS")
    soup = BeautifulSoup(page.content, "html.parser")
    billInfo = soup.find(id="mainBody")

    delegateCell = billInfo.find_all("dd")
    delegateList = delegateCell[1].find_all("a")
    sponsorList = []
    for item in delegateList:
        sponsorList = sponsorList + [item.text]

    sponsoredBills[bill] = sponsorList

print(sponsoredBills)

#Write results to JSON file
inputJSON = json.dumps(sponsoredBills)
resultsfile.write(inputJSON)
resultsfile.close()

# Importing the Required Python libraries
import requests
from bs4 import BeautifulSoup
import urllib.parse

class Reports():

    def __init__(self, address):
        self.findCases(address)

    def findCases(self, address):

        URL = 'https://ncov2019.live/data/unitedstates'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        state = address.split(", ")
        state_name = state[0].capitalize()
        cases = soup.findAll('td', class_ = 'text--gray')
        case_result = self.returnCase(cases, state_name)
        if not bool(case_result):
            print("Place not found for reports\n")
            return
        case_parent = case_result.parent

        confirmed = case_parent.find_all('td', class_ = 'text--green')[0].get_text().strip()
        deceased = case_parent.find_all('td', class_ = 'text--red')[0].get_text().strip()
        print("Confirmed: " + confirmed + "\nDeaths: " + deceased)
        
    
    def returnCase(self, cases, state):
        for case in cases:
            if 'class' in case.attrs:
                if not "save-button" in case.attrs['class']:
                    if case.text.strip("★\r\n ") == state:
                        return case

        return False
        


        

            
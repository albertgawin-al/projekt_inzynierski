import requests
from xml.etree import ElementTree

from settings import *
from .urls import *

class EAPI: 
    def esearch(self, term=''):
        params = {
            "api_key": API_KEY, "db": "pubmed", "term": term, 
            "reldate": 1095, "datetype": "edat", "retmax": 1000,
            "usehistory": "y"
        }
        response = requests.get(esearch_url, params=params)
        root = ElementTree.fromstring(response.text)
        response.close()

        IdList = [Id.text for Id in root.find('IdList')]
        return IdList
    
    def efetch(self, ids):
        params = {
            "api_key": API_KEY, "db": "pubmed", "id": ','.join(ids), 
            "retmax": 1000, "usehistory": "y"
        }
        charRemove = ['<i>','</i>','<b>','</b>','<u>','</u>','<sup>','</sup>',
                      '<sub>','</sub>',]

        response = requests.post(efetch_url, data=params, )
        responseText = response.text

        for char in charRemove:
            responseText = responseText.replace(char, '')
        root = ElementTree.fromstring(responseText)
        response.close()

        articles = root.findall("PubmedArticle")

        return articles

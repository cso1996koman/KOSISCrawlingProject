import json
from UrlObjectFactory import UrlObjectFactory
from KosisUrl import KosisUrl
import re
    
class JsonReader:
    def read_json_file(file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def create_kosis_urls(json_data: dict) -> list:
        kosisUrlList : list = [] 
        kosisUrls = json_data.get('KOSISURL', [])
        for entry in kosisUrls:
            for name, url in entry.items():
                factory = UrlObjectFactory(url)
                kosis_url = factory.createKosisUrl()
                kosisUrlList.append(kosis_url)
                print(kosis_url.getFullUrl())
        return kosisUrlList
    
    def create_kosis_apikey(json_data: dict) -> str:
        return json_data.get('KOSISKEY', '')
    
    def splitStrbyComma(self, str) -> list:
        return str.split(',')
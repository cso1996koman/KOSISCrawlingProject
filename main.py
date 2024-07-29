from JsonReader import JsonReader
from UrlObjectFactory import UrlObjectFactory
from KosisUrl import KosisUrl
from Crawler import Crawler


def main():
    jsonUrls = JsonReader.read_json_file('Urls.json')
    jsonApiKey = JsonReader.read_json_file('Apikey.json')
    apiKey = JsonReader.create_kosis_apikey(jsonApiKey)
    kosisUrls = JsonReader.create_kosis_urls(jsonUrls)
    for url in kosisUrls:
        url.setApiKey(apiKey)
        crawler = Crawler(url.getFullUrl())
        crawler.crawl()
        
    

if __name__ == '__main__':
    main()



    

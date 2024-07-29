from JsonReader import JsonReader
from UrlObjectFactory import UrlObjectFactory
from KosisUrl import KosisUrl



def main():
    jsonUrls = JsonReader.read_json_file('Urls.json')
    jsonApiKey = JsonReader.read_json_file('')
    apiKey = JsonReader.create_kosis_apikey('')
    kosisUrls = JsonReader.create_kosis_urls(jsonUrls)
    
    for url in kosisUrls:
        print(url.getFullUrl())

if __name__ == '__main__':
    main()

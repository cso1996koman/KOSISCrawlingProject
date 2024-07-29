
import json
import pandas as pd
import os
import requests
import xml.etree.ElementTree as ET

class Crawler:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.response = None
        self.jsonResponse = None
    
    def crawl(self):
        self.response = requests.get(self.url, headers=self.headers)
        self.jsonResponse = self.parse_response()
        self.save_as_csv(self.jsonResponse)

    def save_as_csv(self, jsonData):
        df = pd.DataFrame(jsonData)

        files = [f for f in os.listdir('.') if f.startswith('data_') and f.endswith('.csv')]
        if files:
            max_num = max([int(f.split('_')[1].split('.')[0]) for f in files])
            next_num = max_num + 1
        else:
            next_num = 1
        file_name = f'data_{next_num}.csv'
        df.to_csv(file_name, index=False)
        print(f'Saved JSON response as {file_name}')

    def parse_response(self):
        if self.response.status_code == 200:
            content_type = self.response.headers.get('Content-Type')
            main_content_type = content_type.split(';')[0] if content_type else None

            if main_content_type == 'application/json' or main_content_type == 'text/html':
                try:
                    data = json.loads(self.response.text)
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e} - Error Code: {self.response.status_code}")
            elif main_content_type == 'application/xml' or main_content_type == 'text/xml':
                try:
                    error_root = ET.fromstring(self.response.text)
                    error_code = error_root.find('.//err').text if error_root.find('.//err') is not None else 'Unknown'
                    error_msg = error_root.find('.//errMsg').text if error_root.find('.//errMsg') is not None else 'No error message'
                    print(f"Request URL: {self.url}")
                    print(f"XML Error Code: {error_code}")
                    print(f"XML Error Message: {error_msg}")
                except ET.ParseError as inner_e:
                    print(f"Failed to parse XML error message: {inner_e}")
                    print(f"Failed to parse XML error message: {inner_e}")
            else:
                print(f"Error: Unsupported Content-Type - Error Code: {self.response.status_code}")
        else:
            print(f"Error: Received status code {self.response.status_code}")
        
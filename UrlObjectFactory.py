import re
from urllib.parse import urlparse, parse_qs, urlunparse
import KosisUrl

class UrlObjectFactory:
    def __init__(self,fullUrl):
        self.fullUrl = fullUrl
        
    def createKosisUrl(self) -> KosisUrl:
        baseUrl = self.extract_base_url()
        apiKey = self.extractParameter(r'apiKey=[^&]*')
        orgId = self.extractParameter(r'orgId=[^&]*')
        tblId = self.extractParameter(r'tblId=[^&]*')
        objL1 = self.extractParameter(r'objL1=[^&]*')
        objL2 = self.extractParameter(r'objL2=[^&]*')
        objL3 = self.extractParameter(r'objL3=[^&]*')
        objL4 = self.extractParameter(r'objL4=[^&]*')
        objL5 = self.extractParameter(r'objL5=[^&]*')
        objL6 = self.extractParameter(r'objL6=[^&]*')
        objL7 = self.extractParameter(r'objL7=[^&]*')
        objL8 = self.extractParameter(r'objL8=[^&]*')
        itmId = self.extractParameter(r'itmId=[^&]*')
        prdSe = self.extractParameter(r'PrdSe=[^&]*')
        startPrdDe = self.extractParameter(r'startPrdDe=[^&]*')
        endPrdDe = self.extractParameter(r'endPrdDe=[^&]*')
        newEstPrdCnt = self.extractParameter(r'newEstPrdCnt=[^&]*')
        prdInterval = self.extractParameter(r'prdInterval=[^&]*')
        format = self.extractParameter(r'format=[^&]*')
        jsonVD = self.extractParameter(r'jsonVD=[^&]*')
        return KosisUrl(baseUrl, apiKey, itmId, objL1, objL2, objL3, objL4, objL5, objL6, objL7, objL8, format, jsonVD, prdSe, startPrdDe, endPrdDe, orgId, tblId)
    
    def extract_base_url(self) -> str:
        parsed_url = urlparse(self.fullUrl)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', 'method=getList', ''))
        return base_url
        
    def extractParameter(self, pattern: str) -> str:
        match = re.search(pattern, self.fullUrl)
        return match.group(0).split('=')[1] if match else None
    
    
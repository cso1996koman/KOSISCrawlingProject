class KosisUrl:
        def __init__(self, baseUrl, apiKey, itmId, objL1, objL2, objL3, objL4, objL5, objL6, objL7, objL8, format, jsonVD, prdSe, startPrdDe, endPrdDe, orgId, tblId):
            self.baseUrl = baseUrl
            self.apiKey = apiKey
            self.itmId = itmId
            self.objL1 = objL1
            self.objL2 = objL2
            self.objL3 = objL3
            self.objL4 = objL4
            self.objL5 = objL5
            self.objL6 = objL6
            self.objL7 = objL7
            self.objL8 = objL8
            self.format = format
            self.jsonVD = jsonVD
            self.prdSe = prdSe
            self.startPrdDe = startPrdDe
            self.endPrdDe = endPrdDe
            self.orgId = orgId
            self.tblId = tblId
        def getFullUrl(self) -> str:
            return self.baseUrl + "&apiKey=" + self.apiKey + "&itmId= " + self.itmId + "&objL1= " + self.objL1 + "&objL2= " + self.objL2 + "&objL3= " + self.objL3 + "&objL4= " + self.objL4 + "&objL5= " + self.objL5 + "&objL6= " + self.objL6 + "&objL7= " + self.objL7 + "&objL8= " + self.objL8 + "&format= " + self.format + "&jsonVD= " + self.jsonVD + "&PrdSe= " + self.prdSe + "&startPrdDe= " + self.startPrdDe + "&endPrdDe= " + self.endPrdDe + "&orgId= " + self.orgId + "&tblId= " + self.tblId
        def setApiKey(self, apiKey: str):
            self.apiKey = apiKey
        def setItmId(self, itmId: str):
            self.itmId = itmId
        def setObjL1(self, objL1: str):
            self.objL1 = objL1
        def setObjL2(self, objL2: str):
            self.objL2 = objL2
        def setObjL3(self, objL3: str):
            self.objL3 = objL3
        def setObjL4(self, objL4: str):
            self.objL4 = objL4
        def setObjL5(self, objL5: str):
            self.objL5 = objL5
        def setObjL6(self, objL6: str):
            self.objL6 = objL6
        def setObjL7(self, objL7: str):
            self.objL7 = objL7
        def setObjL8(self, objL8: str):
            self.objL8 = objL8
        def setFormat(self, format: str):
            self.format = format
        def setJsonVD(self, jsonVD: str):
            self.jsonVD = jsonVD
        def setPrdSe(self, prdSe: str):
            self.prdSe = prdSe
        def setStartPrdDe(self, startPrdDe: str):
            self.startPrdDe = startPrdDe
        def setEndPrdDe(self, endPrdDe: str):
            self.endPrdDe = endPrdDe
        def setOrgId(self, orgId: str):
            self.orgId = orgId
        def setTblId(self, tblId: str):
            self.tblId = tblId
        def getApiKey(self) -> str:
            return self.apiKey
        def getItmId(self) -> str:
            return self.itmId
        def getObjL1(self) -> str:
            return self.objL1   
        def getObjL2(self) -> str:
            return self.objL2
        def getObjL3(self) -> str:
            return self.objL3
        def getObjL4(self) -> str:
            return self.objL4
        def getObjL5(self) -> str:
            return self.objL5
        def getObjL6(self) -> str:
            return self.objL6
        def getObjL7(self) -> str:
            return self.objL7
        def getObjL8(self) -> str:
            return self.objL8
        def getFormat(self) -> str:
            return self.format
        def getJsonVD(self) -> str:
            return self.jsonVD
        def getPrdSe(self) -> str:
            return self.prdSe
        def getStartPrdDe(self) -> str:
            return self.startPrdDe
        def getEndPrdDe(self) -> str:
            return self.endPrdDe
        def getOrgId(self) -> str:
            return self.orgId
        def getTblId(self) -> str:
            return self.tblId
        def __repr__(self):
            return f"KosisUrl(baseUrl={self.baseUrl}, apiKey={self.apiKey}, itmId={self.itmId}, objL1={self.objL1}, objL2={self.objL2}, objL3={self.objL3}, objL4={self.objL4}, objL5={self.objL5}, objL6={self.objL6}, objL7={self.objL7}, objL8={self.objL8}, format={self.format}, jsonVD={self.jsonVD}, prdSe={self.prdSe}, startPrdDe={self.startPrdDe}, endPrdDe={self.endPrdDe}, orgId={self.orgId}, tblId={self.tblId})"

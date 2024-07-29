import pandas_datareader.data as web
import yfinance as yf
import concurrent.futures
import requests
import datetime
import calendar
import numpy as np
import pandas as pd
import mariadb
import pymysql
import asyncio
from datetime import datetime
import pdb

class getData:
    def __init__(self,name,prdSe,start=None,end=None):
        '''
        name : 사회경제 지표명
        prdSe : 수록주기
        newEstPrdCnt : 불러올 데이터 개수(최근 수록 시점 기준)
        start : 불러올 데이터 시작 시점
        end : 불러올 데이터 종료 시점
        apiInfo : api 호출 파라미터
        url : url
        key : open key
        '''
        self.name=name
        self.prdSe=prdSe
        job_list=pd.read_excel('job_list.xlsx',sheet_name=['main'])['main'].set_index('name')
        source=pd.read_excel('job_list.xlsx',sheet_name=['source'])['source'].set_index('source')
        auxil=pd.read_excel('job_list.xlsx',sheet_name=['auxil'])['auxil'].set_index('name')
        prdSe=pd.read_excel('job_list.xlsx',sheet_name=['prdSe'])['prdSe'].set_index('name')
        index=(prdSe.index==name)
        if prdSe[index][self.prdSe].values[0] == 1:
            pass
        else:
            assert False, 'Error! please check input priod parameter.'

        self.source=job_list[index]['source'].values[0]
        if self.source == 'KOSIS':
            self.fields=auxil['fields'][0].split(',')
            self.itmId=job_list[index]['itmId'].values[0]
            self.orgId=str(int(job_list[index]['orgId'].values[0]))
            self.tblId=job_list[index]['tblId'].values[0]
            self.objL2=job_list[index]['objL2'].values[0]
            self.objL3=job_list[index]['objL3'].values[0]
            if self.objL2 !='ALL':
                self.objL2=''
            if self.objL3 !='ALL':
                self.objL3=''
        elif self.source == 'pandas_datareader':
            self.code = job_list[index]['code'].values[0]
        self.url=source.loc[self.source]['url']
        self.apiKey=source.loc[self.source]['apiKey']

        if (start!=None) and (end==None):
            end=start  #오늘날짜
        elif (start==None) and (end!=None):
            start=end
        elif (start!=None) and (end!=None):
            grepCnt=1
        else:
            assert False, 'Error! please check input parameters.'
        self.grepCnt=int(grepCnt)
        self.start=start
        self.end=end

    def KOSIS(self): #국가통계포탈
        params = {
            'method': 'getList',
            'apiKey': self.apiKey,
            'itmId': self.itmId,
            'objL1': 'ALL',
            'objL2': self.objL2,
            'objL3': self.objL3,
            'objL4': '',
            'objL5': '',
            'objL6': '',
            'objL7': '',
            'objL8': '',
            'format': 'json',
            'jsonVD': 'Y',
            'prdSe': self.prdSe,
            'startPrdDe': self.start,     #시작
            'endPrdDe': self.end,         #끝
            'newEstPrdCnt': '',           #최신날짜를 기준으로 반환하는 데이터 숫자갯수
            'orgId': self.orgId,          #원천 데이터를 제공하는 기관의 아이디 코드
            'tblId': self.tblId
        }

        # GET 요청 보내기
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            try:
                data = pd.DataFrame(response.json())
            except:
                assert False, f"err code : {response.json()['err']}, err msg: {response.json()['errMsg']}"
        else:
            assert False, "Error! Failed to retrieve data: ".format(response.status_code)

        print(f'job : {self.name}, start : {self.start}, end : {self.end}, source : KOSIS , successful download data.')
        return data

    def pandas(self): #미국 연방 준비은행
        data=web.DataReader(self.code, 'fred', self.convert_date(self.start), self.convert_date(self.end))
        data.reset_index(inplace=True)
        data.columns=[['DATE','VALUE']]
        data['DATE'] = data['DATE'].astype(str)
        data['VALUE']=np.round(data['VALUE'],2)
        print(f'job : {self.name}, start : {self.start}, end : {self.end}, source : pandas(FED) , successful download data.')
        return data

    def yahoo(self):
        data=yf.download('KRW=X', start=self.convert_date(self.start), end=self.convert_date(self.end))['Adj Close']
        data=data.reset_index().rename(columns={'Date': 'DATE', 'Adj Close': 'VALUE'})
        data['DATE'] = pd.to_datetime(data['DATE']).dt.strftime('%Y-%m-%d')
        data['VALUE']=np.round(data['VALUE'],2)
        print(f'job : {self.name}, start : {self.start}, end : {self.end}, source : yahoo finance, successful download data.')
        return data

    def convert_date(self,date):
        # 입력값의 길이에 따라 변환 방식 결정
        if len(date) == 4:  # 'YYYY' 형식
            return date
        elif len(date) == 6:  # 'YYYYMM' 형식
            return date[:4]+'-'+date[4:6]
        elif len(date) == 8:  # 'YYYYMMDD' 형식
            return date[:4]+'-'+date[4:6]+'-'+date[6:8]
        else:
            raise ValueError("Invalid date format")

def adjust_date_format(start, end, priod):
    if priod == 'Y':
        start = start[:4]  # 연도만 추출
        end = end[:4]
    elif priod == 'Q':
        start_year = start[:4]
        end_year = end[:4]
        # start_month와 end_month가 모두 주어진 경우 해당 분기 계산
        start_month = int(start[4:6]) if len(start) >= 6 else 1  # start_month가 있으면 가져오고, 없으면 1월로 설정
        end_month = int(end[4:6]) if len(end) >= 6 else 12  # end_month가 있으면 가져오고, 없으면 12월로 설정
        # 각 분기별 시작 월과 끝 월 설정
        start_quarter = (start_month - 1) // 3 + 1
        end_quarter = (end_month - 1) // 3 + 1
        start = f"{start_year}{start_quarter:02}"  # 두 자리 숫자로 포맷팅
        end = f"{end_year}{end_quarter:02}"  # 두 자리 숫자로 포맷팅
    elif priod == 'M':
        start = start[:6] if len(start) >= 6 else start[:4] + '01'  # 연도와 월 추출, 없으면 1월로 가정
        end = end[:6] if len(end) >= 6 else end[:4] + '12'  # 월별이면 월 마지막 날짜로 설정
    elif priod == 'D':
        if len(start) == 4:
            start = start + '0101'
        elif len(start) == 6:
            start = start + '01'
        if len(end) == 4:
            end = end + '1231'
        elif len(end) == 6:
            year = int(end[:4])
            month = int(end[4:6])
            last_day = calendar.monthrange(year, month)[1]
            end = f"{year}{month:02}{last_day:02}"
        elif len(end) == 8:
            year = int(end[:4])
            month = int(end[4:6])
            day = int(end[6:8])
            last_day = calendar.monthrange(year, month)[1]
            if day > last_day:
                end = f"{year}{month:02}{last_day:02}"
    else:
        raise ValueError("Invalid priod value. Allowed values are: 20210101, 202101, 2021")

    return start, end

def dbcon(): ##Connect to MariaDB Platform
    try:
        conndb = mariadb.connect(
            user="smart",
            password="Emsrnfma~~!",
            host="neonet.iptime.org",
            port=33406,
            database="smart")
    except:
        assert False, "Error connecting to MariaDB Platform"
    return conndb

def pushdata(data,job):
    job_list=pd.read_excel('job_list.xlsx',sheet_name=['main'])['main'].set_index('name')
    prdSe=pd.read_excel('job_list.xlsx',sheet_name=['prdSe'])['prdSe'].set_index('name')
    data=data.astype('object')
    idx=data.isna().values
    data[idx]=None

    conndb=dbcon()
    cursor=conndb.cursor()

    query = 'SHOW COLUMNS FROM '+job_list.loc[job]['db_table_name']
    cursor.execute(query)

    db_cols = [row[0] for row in cursor.fetchall()]
    data2=data[db_cols]
    try:
        insert_query = "INSERT INTO " + job_list.loc[job, 'db_table_name'] + f" ({', '.join(db_cols)}) VALUES "
        value_placeholders = ", ".join(['%s'] * len(db_cols))
        update_query = ", ".join([f"{col}=VALUES({col})" for col in db_cols])
        final_query = insert_query + f" ({value_placeholders})" + " ON DUPLICATE KEY UPDATE " + update_query

        # 각 행의 값을 튜플로 변환하여 저장
        values = [tuple(row) for row in data2.itertuples(index=False, name=None)]

        #쿼리 실행
        cursor.executemany(final_query, values)

        # 변경 사항 커밋
        conndb.commit()

        # 연결 종료
        cursor.close()
        conndb.close()
        print('finish data upload')
    except:
        assert False, "데이터 업로드 에러"

def run(job,start,end,priod):
    start,end=adjust_date_format(start, end, priod)
    test=getData(name=job, prdSe=priod, start=start, end=end)
    if test.source == 'KOSIS':
        try:
            data=test.KOSIS()
            pdb.set_trace()
            pushdata(data,job)
        except AssertionError as e:
            if ("31" in str(e)) and (("The requested result cannot exceed 40,000 cells." in str(e)) or ("40,000" in str(e))):
                print(e)
                #날짜 쪼개기
                if priod =='Y':
                    tmp_date = pd.date_range(start=start, end=end, freq='YS').year.tolist()
                    sliced_date = [str(year) for year in tmp_date]
                elif priod =='Q':
                    tmp_date = pd.date_range(start=start[:4]+'Q'+start[5:6], end=end[:4]+'Q'+end[5:6], freq='QS').to_period('Q').tolist()
                    sliced_date = []
                    for period in tmp_date:
                        year = period.year
                        month = period.quarter
                        sliced_date.append(f"{year}0{month}")
                elif priod =='M':
                    tmp_date=adjust_date_format(start, end, 'D')
                    sliced_date=pd.date_range(start=tmp_date[0], end=tmp_date[1], freq='M').strftime('%Y%m').tolist()
                else:
                    assert False, "Error! KOSIS 데이터 40,000셀 초과"

                #쪼갠 날짜로 작업수행
                if len(sliced_date)%2 == 0:
                    for i in range(0,len(sliced_date),2):
                        test=getData(name=job, prdSe=priod, start=sliced_date[i], end=sliced_date[i+1])
                        data=test.KOSIS()
                        pushdata(data,job)
                else:
                    for i in range(0,len(sliced_date),2):
                        if i == np.arange(0,len(sliced_date),2)[-1]:
                            test=getData(name=job, prdSe=priod, start=sliced_date[i], end=sliced_date[-1])
                        else:
                            test=getData(name=job, prdSe=priod, start=sliced_date[i], end=sliced_date[i+1])
                        data=test.KOSIS()
                        pushdata(data,job)
            else:
                assert False, "Error! KOSIS 에러"
    elif test.source == 'pandas_datareader':
        data=test.pandas()
        pushdata(data,job)
    elif test.source == 'yfinance':
        data=test.yahoo()
        pushdata(data,job)
    else:
        assert False, 'Error! please check init configuration.'

def main():
    # job_list=['환율','WTI','한국기준금리','미국기준금리']
    job_list=list(pd.read_excel('job_list.xlsx',sheet_name=['main'])['main'].set_index('name').index)
    prdSe=pd.read_excel('job_list.xlsx',sheet_name=['prdSe'])['prdSe'].set_index('name')
##################################################################
#파라미터 입력
    job='주요경제지표(년)'
    start ='2020'
    end = '2024'
    priod='Y'
    run(job,start,end,priod)
##################################################################
##################################################################
    # start = '2015'
    # end = '2020'
    # for job in job_list:
    #     for priod in list(prdSe.loc[job].dropna().index):
    #         print('=====================================')
    #         print('=====================================')
    #         run(job,start,end,priod)
    #         print('*************************************')
    #         print('*************************************')
##################################################################
##################################################################

if __name__=='__main__':
    main()






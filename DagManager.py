from airflow import DAG
from JsonReader import JsonReader 
from datetime import timedelta
import Crawler
from airflow.operators.python import PythonOperator
import KosisUrl

class DagManager:

    @staticmethod
    def create_dags(json_data: dict, default_args) -> list:
        kosisUrls = JsonReader.create_kosis_urls(json_data)
        dags = [url.create_dag(default_args,url) for url in kosisUrls]
        return dags
    
    def create_dag(self, default_args, kosisUrl : KosisUrl) -> DAG:
        schedule_interval = None
        if kosisUrl.prdSe == 'Y':
            schedule_interval = timedelta(days=365)
        elif kosisUrl.prdSe == 'M':
            schedule_interval = timedelta(days=30)
        elif kosisUrl.prdSe == 'Q':
            schedule_interval = timedelta(days=90)

        dag_id = f"crawl_dag_{kosisUrl.prdSe}_{kosisUrl.tblId}"
        dag = DAG(
            dag_id,
            default_args=default_args,
            description=f'A crawling DAG for {kosisUrl.prdSe}',
            schedule_interval=schedule_interval,
        )
        def crawl_task():
            kosisUrl.setApiKey(JsonReader.read_json_file("Apikey.json"))
            crawler = Crawler(kosisUrl.getFullUrl())
            crawler.crawl()

        crawl_task = PythonOperator(
            task_id='crawl_task',
            python_callable=crawl_task,
            dag=dag,
        )
        return dag
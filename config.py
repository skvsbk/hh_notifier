from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


class Config:
    load_dotenv('.env')
    TG_ID = os.getenv('TG_ID')
    TG_TOKEN = os.getenv('TG_TOKEN')
    TG_URL = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage?'

    HH_URL = 'https://api.hh.ru/vacancies'

    HH_API_SALARY_TO = 120000
    HH_API_TEXT = 'NAME:Python AND NOT(Руководитель OR QA OR Full-Stack)'
    HH_API_SCHEDULE = 'remote'
    HH_API_DATE_FROM = (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")

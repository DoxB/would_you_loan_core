from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_ID = os.environ.get('DB_ID')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_KOOKMIN_PORT = os.environ.get('DB_KOOKMIN_PORT')
DB_WOORI_PORT = os.environ.get('DB_WOORI_PORT')
DB_SHINHAN_PORT = os.environ.get('DB_SHINHAN_PORT')
DB_ETC_PORT = os.environ.get('DB_ETC_PORT')
DB_KOOKMIN = os.environ.get('DB_KOOKMIN')
DB_WOORI = os.environ.get('DB_WOORI')
DB_SHINHAN = os.environ.get('DB_SHINHAN')
DB_ETC = os.environ.get('DB_ETC')

### 국민은행 DB 연결관리부
class KookminEngineconn:
    def __init__(self):
        DB_URL = f'mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_KOOKMIN_PORT}/{DB_KOOKMIN}'
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

### 우리은행 DB 연결관리부
class WooriEngineconn:
    def __init__(self):
        DB_URL = f'mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_WOORI_PORT}/{DB_WOORI}'
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

### 신한은행 DB 연결관리부
class ShinhanEngineconn:
    def __init__(self):
        DB_URL = f'mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_SHINHAN_PORT}/{DB_SHINHAN}'
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

### 나머지 모든 은행 DB 연결관리부
class EtcEngineconn:
    def __init__(self):
        DB_URL = f'mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_ETC_PORT}/{DB_ETC}'
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
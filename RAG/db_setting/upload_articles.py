import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


'''
배치작업을 위해서는 앞부분에 엑셀 파일을 받아오는 코드 구현 필요
'''

####################################
###  엑셀 데이터 DataFrame 변환  ###
####################################

## 엑셀 파일 df 변환
file_path = 'NewsResult_with_sentiment.xlsx'
df = pd.read_excel(file_path, dtype={'뉴스 식별자': str})

## 필요한 열만 남기기
columns_to_keep = ['뉴스 식별자', '일자', '언론사', '제목', '키워드', '본문', 'URL', 'sentiment_desc']
df = df[columns_to_keep]

## '일자' 열을 DATE 형식으로 변환
df['일자'] = pd.to_datetime(df['일자'], format='%Y%m%d').dt.date

## 결측값이 포함된 행 제거
df = df.dropna()

## 컬럼명 변경
df.columns = ['article_id', 'article_date', 'company', 'title', 'keywords', 'content', 'url', 'sentiment']

####################################
###     DataFrame DB 업데이트    ###
####################################

load_dotenv()

# MySQL 데이터베이스 연결 문자열 생성
DB_ID = os.environ.get('DB_ID')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB = os.environ.get('DB')

engine = create_engine(f"mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}")

# DataFrame을 DB 테이블로 업로드
table_name = 'news_articles'
df.to_sql(table_name, con=engine, if_exists='replace', index=False)
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
file_path = 'ujloan_loans_v4.csv'
df = pd.read_csv(file_path)

## 필요한 열만 남기기
columns_to_keep = ['bank_name', 'loan_name', 'repayment_type', 'interest_rate_type', 'interest_rate_min',
                   'interest_rate_max', 'interest_rate_avg', 'loan_limit', 'max_loan_limit', 'max_apartment_price_limit',
                   'loan_additional_cost', 'early_repayment_fee', 'overdue_interest_rate', 'subscription_method', 'max_loan_duration',
                   'financial_sector', 'government_support_type', 'credit_1_interest', 'credit_2_interest', 'credit_3_interest',
                   'credit_4_interest', 'credit_5_interest']
df = df[columns_to_keep]

## 결측값이 포함된 행 제거
df = df.dropna()

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
table_name = 'loans'
df.to_sql(table_name, con=engine, if_exists='replace', index=False)
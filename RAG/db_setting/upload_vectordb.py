from sqlalchemy import create_engine
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.documents import Document
import pandas as pd
import os
from dotenv import load_dotenv
from tqdm import tqdm

####################################
###    DB에서 기사 데이터 받기   ###
####################################

load_dotenv()

# MySQL 데이터베이스 연결 문자열 생성
DB_ID = os.environ.get('DB_ID')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB = os.environ.get('DB')

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{DB_ID}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}")

# 쿼리를 실행하여 DataFrame으로 로드
query = "SELECT article_id, article_date, company, title, url, content FROM news_articles"
df = pd.read_sql(query, engine)


####################################
###   받은 데이터 VectorDB 적재  ###
####################################

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT')
ELASTIC_ID = os.environ.get('ELASTIC_ID')
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')

# 임베딩 모델 설정
embeddings = HuggingFaceEmbeddings(
    model_name="../embedding/model/bge-m3",
    model_kwargs={'device':'cuda'}
)

# ElasticSearch 벡터 스토어 설정
client = ElasticsearchStore(
    es_url=f"http://{ELASTIC_HOST}:{ELASTIC_PORT}",
    index_name="article-index",
    es_user=ELASTIC_ID,
    es_password=ELASTIC_PASSWORD,
    embedding=embeddings)

# 데이터 임베딩 후 ElasticSearch에 적재
for _, row in tqdm(df.iterrows()):
    # 각 문서를 Document 객체로 생성
    doc = Document(
        page_content=row['content'],
        metadata={
            "title": row['title'],
            "article_date": row['article_date'],
            "company": row['company'],
            "url": row['url']
        }
    )
    # ElasticSearch에 문서를 추가하며 article_id를 _id로 설정하여 덮어쓰기
    client.add_documents([doc], ids=[row['article_id']])



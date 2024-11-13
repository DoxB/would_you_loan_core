import os
from dotenv import load_dotenv
import boto3

load_dotenv()

## AWS S3 버킷 접근 정보
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
AWS_STORAGE_OVERRIDE = True
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')

class AwsS3conn:
    def __init__(self):
        self.bucket =  BUCKET_NAME

    def download(self, user_id, file_name):
        ## 다운로드시 서버 저장할 파일 명
        file_path = f'./tmp/{user_id}/{file_name}.pdf'

        ## 파일 경로에서 폴더 경로만 추출
        folder_path = os.path.dirname(file_path)
        ## 폴더가 존재하지 않으면 생성
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        ## 접근할 S3 파일 위치
        key =f'ocr/{user_id}_{file_name}.pdf'

        ## S3 접근 클라이언트 정의
        s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_DEFAULT_REGION
        )

        ## 파일 다운로드
        s3_client.download_file(self.bucket, key, file_path)
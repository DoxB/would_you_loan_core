from fastapi import FastAPI
from s3_conn import AwsS3conn
from items import FileNameRequest
from functions import pdf2img, crop_image, document_ocr

app = FastAPI()

AwsS3_engine = AwsS3conn()

####################################
###    OCR 이후 데이터 보내기    ###
####################################

### OCR 작업
@app.post("/ocr")
async def ocr_service(requset: FileNameRequest):
    user_id = requset.user_id
    file_name = requset.file_name

    AwsS3_engine.download(user_id, file_name)
    pdf2img(user_id, file_name)
    crop_image(user_id, file_name)
    contract_info = document_ocr(user_id)

    return contract_info
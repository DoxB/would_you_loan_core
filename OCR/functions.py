from pdf2image import convert_from_path
import cv2
import easyocr
import shutil

## PDF -> image 로 변환
def pdf2img(user_id, file_name):
    PDF_FILE_PATH = f'./tmp/{user_id}/{file_name}.pdf'

    pages = convert_from_path(PDF_FILE_PATH)
    for i, page in enumerate(pages):
        page.save(f"./tmp/{user_id}/{file_name}_{i}.jpg", "JPEG")

## OCR이 필요한 부분들 짜르기
def crop_image(user_id, file_name):
    # 이미지 로드
    image = cv2.imread(f"./tmp/{user_id}/{file_name}_0.jpg")

    # 왼쪽 상단 모서리 좌표, 오른쪽 하단 모서리 좌표
    crop_range = [('location', [228, 286, 1566, 354]), # 소재지
                ('building_use', [810, 424, 1094, 490]), # 건물 - 용도
                ('exclusive_area', [1350, 422, 1560, 492]), # 건물 - 전용 면적
                ('sale_price', [280, 580, 1560, 632]), # 매매 대금
                ('buyer_address', [346, 1906, 1442, 1968]), # 매수인 - 주소
                ('buyer_name', [1218, 1972, 1438, 2030])] # 매수인 - 이름

    for crop_one in crop_range:
        # 바운딩 박스 영역을 잘라냄
        cropped_image = image[crop_one[1][1]:crop_one[1][3], crop_one[1][0]:crop_one[1][2]]

        # 잘라낸 이미지 저장
        cv2.imwrite(f'./tmp/{user_id}/{crop_one[0]}.jpg', cropped_image)

## OCR 진행
def document_ocr(user_id):
    document_info = dict()

    ## 모델 빌드 (CPU 사용, GPU 자원이 제한적)
    reader = easyocr.Reader(['ko'], gpu=False)

    labels = ['location', 'building_use', 'exclusive_area', 'sale_price', 'buyer_address', 'buyer_name']

    for label in labels:
        result = reader.recognize(f'./tmp/{user_id}/{label}.jpg')
        document_info[label] = result[0][1]

    ## 서버에 받은 PDF 파일, OCR을 위해 생성된 이미지 파일들 삭제
    shutil.rmtree(f'./tmp/{user_id}')

    return document_info
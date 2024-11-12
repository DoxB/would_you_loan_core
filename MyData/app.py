from fastapi import FastAPI
from database import KookminEngineconn, WooriEngineconn, ShinhanEngineconn, EtcEngineconn
from models import KookminLoan, WooriLoan, ShinhanLoan, EtcLoan
from items import KookminLoanItem, WooriLoanItem, ShinhanLoanItem, EtcLoanItem, UserIdRequest, LoanDeleteRequest

app = FastAPI()

kookmin_engine = KookminEngineconn()
woori_engine = WooriEngineconn()
shinhan_engine = ShinhanEngineconn()
etc_engine = EtcEngineconn()


####################################
### 마이데이터 대출정보 끌어오기 ###
####################################

### 대출정보 끌어오기
@app.post("/mydata")
async def get_mydata(request: UserIdRequest):
    ### DB 연결 세션 열기
    kookmin_session = kookmin_engine.sessionmaker()
    woori_session = woori_engine.sessionmaker()
    shinhan_session = shinhan_engine.sessionmaker()
    etc_session = etc_engine.sessionmaker()

    try:
        ### 정보 끌어오기
        user_id = request.user_id
        loan_info = kookmin_session.query(KookminLoan).filter(KookminLoan.user_id == user_id).all()
        loan_info += woori_session.query(WooriLoan).filter(WooriLoan.user_id == user_id).all()
        loan_info += shinhan_session.query(ShinhanLoan).filter(ShinhanLoan.user_id == user_id).all()
        loan_info += etc_session.query(EtcLoan).filter(EtcLoan.user_id == user_id).all()

        return loan_info

    finally:
        ### 세션 종료
        kookmin_session.close()
        woori_session.close()
        shinhan_session.close()
        etc_session.close()


####################################
###      신규대출 업데이트       ###
####################################

### 국민은행 대출 정보 추가
@app.post("/add_kookmin_loan")
async def add_kookmin_loan(request: KookminLoanItem):
    kookmin_session = kookmin_engine.sessionmaker()

    try:
        ### 객체 생성해서 테이블에 추가
        new_loan = KookminLoan(
            user_id=request.user_id,
            bank_name=request.bank_name,
            loan_name=request.loan_name,
            loan_amount=request.loan_amount,
            interest_rate=request.interest_rate,
            loan_start_date=request.loan_start_date,
            loan_end_date=request.loan_end_date,
            loan_status=request.loan_status,
            created_at=request.created_at
        )

        kookmin_session.add(new_loan)
        kookmin_session.commit()
        kookmin_session.refresh(new_loan)

        return {"message": "국민은행 대출 정보 추가 성공", "loan_id": new_loan.loan_id}

    finally:
        kookmin_session.close()

### 우리은행 대출 정보 추가
@app.post("/add_woori_loan")
async def add_woori_loan(request: WooriLoanItem):
    woori_session = woori_engine.sessionmaker()

    try:
        ### 객체 생성해서 테이블에 추가
        new_loan = WooriLoan(
            user_id=request.user_id,
            bank_name=request.bank_name,
            loan_name=request.loan_name,
            loan_amount=request.loan_amount,
            interest_rate=request.interest_rate,
            loan_start_date=request.loan_start_date,
            loan_end_date=request.loan_end_date,
            loan_status=request.loan_status,
            created_at=request.created_at
        )

        woori_session.add(new_loan)
        woori_session.commit()
        woori_session.refresh(new_loan)

        return {"message": "우리은행 대출 정보 추가 성공", "loan_id": new_loan.loan_id}

    finally:
        woori_session.close()

### 신한은행 대출정보 추가
@app.post("/add_shinhan_loan")
async def add_shinhan_loan(request: ShinhanLoanItem):
    shinhan_session = shinhan_engine.sessionmaker()

    try:
        ### 객체 생성해서 테이블에 추가
        new_loan = ShinhanLoan(
            user_id=request.user_id,
            bank_name=request.bank_name,
            loan_name=request.loan_name,
            loan_amount=request.loan_amount,
            interest_rate=request.interest_rate,
            loan_start_date=request.loan_start_date,
            loan_end_date=request.loan_end_date,
            loan_status=request.loan_status,
            created_at=request.created_at
        )

        shinhan_session.add(new_loan)
        shinhan_session.commit()
        shinhan_session.refresh(new_loan)

        return {"message": "신한은행 대출 정보 추가 성공", "loan_id": new_loan.loan_id}

    finally:
        shinhan_session.close()

### 기타 모든 은행 대출 정보 추가
@app.post("/add_etc_loan")
async def add_etc_loan(request: EtcLoanItem):
    etc_session = etc_engine.sessionmaker()

    try:
        ### 객체 생성해서 테이블에 추가
        new_loan = EtcLoan(
            user_id=request.user_id,
            bank_name=request.bank_name,
            loan_name=request.loan_name,
            loan_amount=request.loan_amount,
            interest_rate=request.interest_rate,
            loan_start_date=request.loan_start_date,
            loan_end_date=request.loan_end_date,
            loan_status=request.loan_status,
            created_at=request.created_at
        )

        etc_session.add(new_loan)
        etc_session.commit()
        etc_session.refresh(new_loan)

        return {"message": f"{request.bank_name} 대출 정보 추가 성공", "loan_id": new_loan.loan_id}

    finally:
        etc_session.close()


####################################
###    대환대출 기존대출 삭제    ###
####################################

### 국민은행 대출 삭제
@app.post("/remove_kookmin_loan")
async def remove_kookmin_loan(request: LoanDeleteRequest):
    kookmin_session = kookmin_engine.sessionmaker()

    try:
        del_loan = kookmin_session.query(KookminLoan).filter(KookminLoan.loan_id == request.loan_id).first()

        kookmin_session.delete(del_loan)
        kookmin_session.commit()

        return {"message": "국민은행 대출 정보 삭제 성공", "loan_id": del_loan.loan_id}

    finally:
        kookmin_session.close()

### 우리은행 대출 삭제
@app.post("/remove_woori_loan")
async def remove_woori_loan(request: LoanDeleteRequest):
    woori_session = woori_engine.sessionmaker()

    try:
        del_loan = woori_session.query(WooriLoan).filter(WooriLoan.loan_id == request.loan_id).first()

        woori_session.delete(del_loan)
        woori_session.commit()

        return {"message": "우리은행 대출 정보 삭제 성공", "loan_id": del_loan.loan_id}

    finally:
        woori_session.close()

### 신한은행 대출 삭제
@app.post("/remove_shinhan_loan")
async def remove_shinhan_loan(request: LoanDeleteRequest):
    shinhan_session = shinhan_engine.sessionmaker()

    try:
        del_loan = shinhan_session.query(ShinhanLoan).filter(ShinhanLoan.loan_id == request.loan_id).first()

        shinhan_session.delete(del_loan)
        shinhan_session.commit()

        return {"message": "신한은행 대출 정보 삭제 성공", "loan_id": del_loan.loan_id}

    finally:
        shinhan_session.close()

### 기타 모든 은행 대출 삭제
@app.post("/remove_etc_loan")
async def remove_etc_loan(request: LoanDeleteRequest):
    etc_session = etc_engine.sessionmaker()

    try:
        del_loan = etc_session.query(EtcLoan).filter(EtcLoan.loan_id == request.loan_id).first()

        etc_session.delete(del_loan)
        etc_session.commit()

        return {"message": f"{del_loan.bank_name} 대출 정보 삭제 성공", "loan_id": del_loan.loan_id}

    finally:
        etc_session.close()
from pydantic import BaseModel
from datetime import date

class KookminLoanItem(BaseModel):
    user_id: int
    bank_name: str = None
    loan_name: str = None
    loan_amount: float = None
    interest_rate: float = None
    loan_start_date: date = None
    loan_end_date: date = None
    loan_status: str = None
    created_at: date = None

class WooriLoanItem(BaseModel):
    user_id: int
    bank_name: str = None
    loan_name: str = None
    loan_amount: float = None
    interest_rate: float = None
    loan_start_date: date = None
    loan_end_date: date = None
    loan_status: str = None
    created_at: date = None

class ShinhanLoanItem(BaseModel):
    user_id: int
    bank_name: str = None
    loan_name: str = None
    loan_amount: float = None
    interest_rate: float = None
    loan_start_date: date = None
    loan_end_date: date = None
    loan_status: str = None
    created_at: date = None

class EtcLoanItem(BaseModel):
    user_id: int
    bank_name: str = None
    loan_name: str = None
    loan_amount: float = None
    interest_rate: float = None
    loan_start_date: date = None
    loan_end_date: date = None
    loan_status: str = None
    created_at: date = None

class UserIdRequest(BaseModel):
    user_id: int

class LoanDeleteRequest(BaseModel):
    loan_id: int
    bank_name: str = None
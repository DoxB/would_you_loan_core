from pydantic import BaseModel
from datetime import date

###################
###     대출    ###
###################

class KookminLoanItem(BaseModel):
    user_id: int
    bank_name: str = None
    loan_name: str = None
    loan_category: str = None
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
    loan_category: str = None
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
    loan_category: str = None
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
    loan_category: str = None
    loan_amount: float = None
    interest_rate: float = None
    loan_start_date: date = None
    loan_end_date: date = None
    loan_status: str = None
    created_at: date = None

###################
###   예적금    ###
###################

class KookminAccounItem(BaseModel):
    user_id: int
    bank_name: str = None
    account_name: str = None
    balance: float = None
    account_type: str = None
    created_at: date = None

class WooriAccounItem(BaseModel):
    user_id: int
    bank_name: str = None
    account_name: str = None
    balance: float = None
    account_type: str = None
    created_at: date = None

class ShinhanAccounItem(BaseModel):
    user_id: int
    bank_name: str = None
    account_name: str = None
    balance: float = None
    account_type: str = None
    created_at: date = None

class EtcAccounItem(BaseModel):
    user_id: int
    bank_name: str = None
    account_name: str = None
    balance: float = None
    account_type: str = None
    created_at: date = None


class UserIdRequest(BaseModel):
    user_id: int

class LoanDeleteRequest(BaseModel):
    user_id: int
    loan_name: str
    loan_amount: int
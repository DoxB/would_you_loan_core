from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

###################
###  대출 정보  ###
###################

class KookminLoan(Base):
    __tablename__ = "kookmin_loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(20), nullable=True)
    loan_name = Column(String(100), nullable=True)
    loan_category = Column(String(20), nullable=True)
    loan_amount = Column(DECIMAL(15, 0), nullable=True)
    interest_rate = Column(DECIMAL(4, 2), nullable=True)
    loan_start_date = Column(Date, nullable=True)
    loan_end_date = Column(Date, nullable=True)
    loan_status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class WooriLoan(Base):
    __tablename__ = "woori_loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(20), nullable=True)
    loan_name = Column(String(100), nullable=True)
    loan_category = Column(String(20), nullable=True)
    loan_amount = Column(DECIMAL(15, 0), nullable=True)
    interest_rate = Column(DECIMAL(4, 2), nullable=True)
    loan_start_date = Column(Date, nullable=True)
    loan_end_date = Column(Date, nullable=True)
    loan_status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class ShinhanLoan(Base):
    __tablename__ = "shinhan_loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(20), nullable=True)
    loan_name = Column(String(100), nullable=True)
    loan_category = Column(String(20), nullable=True)
    loan_amount = Column(DECIMAL(15, 0), nullable=True)
    interest_rate = Column(DECIMAL(4, 2), nullable=True)
    loan_start_date = Column(Date, nullable=True)
    loan_end_date = Column(Date, nullable=True)
    loan_status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class EtcLoan(Base):
    __tablename__ = "etc_loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(20), nullable=True)
    loan_name = Column(String(100), nullable=True)
    loan_category = Column(String(20), nullable=True)
    loan_amount = Column(DECIMAL(15, 0), nullable=True)
    interest_rate = Column(DECIMAL(4, 2), nullable=True)
    loan_start_date = Column(Date, nullable=True)
    loan_end_date = Column(Date, nullable=True)
    loan_status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

###################
### 예적금 정보 ###
###################

class KookminAccount(Base):
    __tablename__ = "kookmin_accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    balance = Column(DECIMAL(15, 0), nullable=True)
    account_type = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class WooriAccount(Base):
    __tablename__ = "woori_accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    balance = Column(DECIMAL(15, 0), nullable=True)
    account_type = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class ShinhanAccount(Base):
    __tablename__ = "shinhan_accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    balance = Column(DECIMAL(15, 0), nullable=True)
    account_type = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

class EtcAccount(Base):
    __tablename__ = "etc_accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    balance = Column(DECIMAL(15, 0), nullable=True)
    account_type = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)
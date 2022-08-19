from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, Date, String, Boolean, BigInteger
from sqlalchemy.orm import relationship

from database.config import Base


class Service(Base):
    __tablename__ = 'services'

    id: int = Column(Integer, primary_key=True)
    percent: float | None = Column(Float, nullable=True, default=0.00)
    usd_percent: float | None = Column(Float, nullable=True, default=0.00)
    min_btc: int | None = Column(Integer, nullable=True, default=0)
    min_usd: int | None = Column(Integer, nullable=False, default=0)
    cashback_percent: float | None = Column(Float, nullable=True, default=0.00)
    btc_limit: int | None = Column(Integer, nullable=True, default=0)
    usd_limit: int | None = Column(Integer, nullable=True, default=0)
    main_photo: str | None = Column(String(100), nullable=True, default='')


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, unique=True, index=True, primary_key=True)
    chat_id: int = Column(BigInteger, nullable=False, unique=True, index=True)
    username: str = Column(String(100), nullable=True)
    count_trades: int = Column(Integer, default=0)
    sum_trades: float = Column(Float, default=0)
    cashback: float = Column(Float, default=0)
    is_admin: bool = Column(Boolean, default=False)
    is_banned: bool = Column(Boolean, default=False)
    date_created: datetime = Column(Date, default=datetime.utcnow)

    transactions = relationship(
        'Transaction', back_populates='user', cascade='all, delete-orphan'
    )


class Transaction(Base):
    __tablename__ = 'transactions'

    id: int = Column(Integer, primary_key=True)
    amount: float = Column(Float)
    price: float = Column(Float)
    total: float = Column(Float)
    date_created: datetime = Column(Date, default=datetime.utcnow)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    status: int = Column(Integer, default=2)
    address: str = Column(String(100))
    type: int = Column(Integer)
    network: int = Column(Integer)
    photo: str | None = Column(String(100), nullable=True)

    user = relationship(
        'User', back_populates='transactions'
    )


class Requisites(Base):
    __tablename__ = 'requisites'

    id: int = Column(Integer, primary_key=True)
    data: str = Column(String(250))
    info: str = Column(String(250))
    type: int = Column(Integer)

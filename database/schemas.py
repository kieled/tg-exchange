from datetime import datetime
from pydantic import BaseModel


class TransactionIn(BaseModel):
    type: int
    network: int | None = None
    amount: float
    address: str
    total: float
    price: float
    date_created: datetime = datetime.now()
    user_id: int
    status: int = 2
    photo: str
    cashback: int | None = None


class RequisitesIn(BaseModel):
    data: str | None = None
    info: str | None = None


class RequisitesOut(RequisitesIn):
    class Config:
        orm_mode = True


class ServiceIn(BaseModel):
    percent: float | None = None
    usd_percent: float | None = None
    min_btc: int | None = None
    min_usd: int | None = None
    cashback_percent: float | None = None
    btc_limit: int | None = None
    usd_limit: int | None = None
    main_photo: str | None = None


class ServiceOut(ServiceIn):
    class Config:
        orm_mode = True


class UserIn(BaseModel):
    chat_id: int
    username: str | None = None

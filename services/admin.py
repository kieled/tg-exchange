from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import User, Transaction, Service, Requisites
from database.schemas import ServiceIn, RequisitesIn


class AdminService:
    def __init__(self, session: Session):
        self.db = session

    def service(self) -> Service:
        service = self.db.query(Service).filter(Service.id == 1).first()
        if not service:
            item = Service(id=1)
            self.db.add(item)
            self.db.commit()
            return item
        return service

    def user(self, id: int) -> User:
        user = self.db.query(User).filter(User.chat_id == id).first()
        if not user:
            raise HTTPException(status_code=404)
        return user

    def user_by_id(self, id: int) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404)
        return user

    def user_by_username(self, username: str):
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404)
        return user

    def admins(self) -> list[int]:
        ids = []
        for user in self.db.query(User.chat_id).filter(User.is_admin == 1).all():
            ids.append(user.chat_id)
        return ids

    def transaction(self, id: int) -> Transaction:
        transaction = self.db.query(Transaction).filter(Transaction.id == id).first()
        if not transaction:
            raise HTTPException(status_code=404)
        return transaction

    def confirm_transaction(self, id: int):
        trans = self.transaction(id)
        trans.status = 1
        user = self.user_by_id(trans.user_id)
        service = self.service()
        user.cashback = user.cashback + (trans.total * service.cashback_percent)
        user.count_trades += 1
        user.sum_trades += trans.total
        self.db.commit()

    def cancel_transaction(self, id: int):
        trans = self.transaction(id)
        trans.status = 3
        self.db.commit()

    def update_service(self, updated_service: ServiceIn):
        self.db.query(Service).filter(Service.id == 1).update(updated_service.dict(exclude_unset=True))
        self.db.commit()

    def block_user(self, id: int):
        user = self.user_by_id(id)
        user.is_banned = not user.is_banned
        self.db.commit()

    def change_transaction_status(self, id: int):
        transaction = self.transaction(id)
        transaction.status = 2
        self.db.commit()

    def _requisites(self) -> Requisites:
        data = self.db.query(Requisites).filter(Requisites.id == 1).first()
        if not data:
            item = Requisites(id=1, data='', info='', type=1)
            self.db.add(item)
            self.db.commit()
            return item
        return data

    def update_requisites(self, data: RequisitesIn):
        requisites = self._requisites()
        if data.data:
            requisites.data = data.data
        if data.info:
            requisites.info = data.info
        self.db.commit()

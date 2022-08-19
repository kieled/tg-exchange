from sqlalchemy import func
from sqlalchemy.orm import Session
from database.models import User, Transaction, Requisites
from database.schemas import TransactionIn, UserIn


class UserService:
    def __init__(self, session: Session):
        self.db = session

    def user(self, id: int) -> User | None:
        try:
            user = self.db.query(User).filter(User.chat_id == id).first()
            return user
        except:
            return None

    def create_user(self, data: UserIn) -> User:
        user = User(**data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def cashback(self, id: int) -> int:
        return self.db.query(User.cashback).filter(User.chat_id == id).scalar()

    def transactions_count(self, id: int) -> int:
        user = self.user(id)
        return self.db.query(func.count('*')).select_from(Transaction).filter(Transaction.user_id == user.id).scalar()

    def transactions(self, id: int, page: int) -> list[Transaction]:
        user = self.user(id)
        return self.db.query(Transaction).filter(
            Transaction.user_id == user.id).limit(3).offset((page - 1) * 3).all()

    def complete_transactions(self, user_id: int, page: int):
        transactions = self.transactions(user_id, page)
        count = self.transactions_count(user_id)
        return {
            'count': count,
            'result': transactions
        }

    def create_transaction(self, data: TransactionIn) -> int:
        user = self.user(data.user_id)

        if data.cashback:
            data.total = data.total - data.cashback
            user.cashback = user.cashback - data.cashback
        data.user_id = user.id
        transaction = Transaction(**data.dict(exclude={'cashback'}))
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction.id

    def requisites(self) -> Requisites:
        requisites = self.db.query(Requisites).filter(Requisites.id == 1).first()
        if not requisites:
            item = Requisites(id=1, data='', info='', type=1)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        return requisites

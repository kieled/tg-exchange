from database.models import User, Transaction, Requisites, Service
from services.admin import AdminService
from services.user import UserService
from database.config import session
from database.schemas import RequisitesIn, TransactionIn, ServiceIn, UserIn


def users(func):
    def wrapper(*args, **kwargs):
        with session() as db:
            service = UserService(session=db)
            return func(service, *args, **kwargs)

    return wrapper


def admins(func):
    def wrapper(*args, **kwargs):
        with session() as db:
            service = AdminService(session=db)
            return func(service, *args, **kwargs)

    return wrapper


@users
def get_requisites(service: UserService) -> Requisites:
    return service.requisites()


@admins
def update_requisites(service: AdminService, values: dict):
    values = RequisitesIn(**values)
    service.update_requisites(values)


@admins
def get_btc_price(service: AdminService) -> float:
    return float(service.service().percent)


@admins
def get_usd_price(service: AdminService) -> float:
    return float(service.service().usd_percent)


@users
def get_cashback_info(service: UserService, value: int) -> int:
    return service.cashback(value)


@users
def get_user_info(service: UserService, user_id: int) -> User | None:
    return service.user(user_id)


@users
def create_user(service: UserService, data: UserIn) -> User:
    return service.create_user(data)


@users
def get_user_transactions(service: UserService, user_id: int, page: int = 1) -> Transaction:
    return service.complete_transactions(user_id, page)


@users
def create_order_api(service: UserService, order: dict) -> int:
    order = TransactionIn(**order)
    return service.create_transaction(order)


@admins
def update_service_api(service: AdminService, data: dict):
    data = ServiceIn(**data)
    service.update_service(data)


@admins
def get_service_api(service: AdminService) -> Service:
    return service.service()


@admins
def get_admins(service: AdminService) -> list[int]:
    return service.admins()


@admins
def admin_get_transaction(service: AdminService, transaction_id: int) -> Transaction | None:
    try:
        return service.transaction(transaction_id)
    except:
        return None


@admins
def admin_get_user(service: AdminService, user_id: int) -> User | None:
    try:
        return service.user(user_id)
    except:
        return None


@admins
def admin_get_user_by_username(service: AdminService, username: str) -> User | None:
    try:
        return service.user_by_username(username)
    except:
        return None


@admins
def admin_get_user_by_id(service: AdminService, user_id: int) -> User:
    return service.user_by_id(user_id)


@admins
def admin_block_user(service: AdminService, user_id: int):
    service.block_user(user_id)


@admins
def admin_change_status(service: AdminService, trans_id: int):
    service.change_transaction_status(trans_id)


@admins
def complete_transaction(service: AdminService, transaction_id: int):
    service.confirm_transaction(transaction_id)


@admins
def cancel_transaction(service: AdminService, transaction_id: int):
    service.cancel_transaction(transaction_id)

from datetime import datetime
from typing import Dict, Union
from tg_app.api import get_btc_price, get_usd_price
from tg_app.localization import calculator_result


def get_currency(type: int):
    currency = ['BYN', 'BTC', 'BYN', 'USDT']
    return currency[type - 1]


class Calculator:
    def __init__(self):
        self._type_transfer: Dict[int, int] = {}
        self._last_updated: datetime = datetime.now()
        self._price: int | float | None = None
        self._usd_price: float | None = None
        self._count: int = 0

        self._fetch()

    def set(self, value: int, user_id: int):
        self._type_transfer[user_id] = value

    def convert(self, value: float, user_id: int | None = None) -> Union[float, int]:
        currency = self._type_transfer[user_id]
        price = self.get_price()['price'] if currency == 1 or currency == 2 else self.get_price()['usd_price']
        price = float(price)
        if currency == 1 or currency == 4:
            rounding = 1
        elif currency == 2:
            rounding = 6
        else:
            rounding = 2
        if currency == 3 or currency == 1:
            return round(value * price, rounding)
        else:
            return round(value / price, rounding)

    def _fetch(self):
        self._price = get_btc_price()
        self._usd_price = get_usd_price()

    def get_price(self) -> dict:
        self._fetch()
        return {
            'price': self._price,
            'usd_price': self._usd_price
        }

    def clear(self, user_id: int):
        if self._type_transfer.get(user_id):
            del self._type_transfer[user_id]

    def calculate(self, user_id: int, value: float):
        type = self._type_transfer.get(user_id)
        value = self.convert(value, user_id)
        text = calculator_result(value, get_currency(type))
        self.clear(user_id)
        return text


calculator = Calculator()

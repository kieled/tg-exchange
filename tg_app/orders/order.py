def get_round(c: int, t: int):
    if (c + t - 1) == 1:
        return 1
    else:
        if c == 2 and t == 1:
            return 6
        else:
            return 2


class Order:
    def __init__(self):
        self._type: dict[int: int] = {}  # BTC / USD-T
        self._currency: dict[int: int] = {}  # (BTC / BYN) / (USD / BYN)
        self._network: dict[int: int] = {}  # TRC-20 / ERC-20
        self._amount: dict[int: float] = {}  # USER INPUT AMOUNT
        self._total: dict[int: float] = {}  # ORDER TOTAL PRICE
        self._btc_adr: dict[int: str] = {}  # USER INPUT ADDRESS (USD-T / BTC)
        self._price: dict[int: float] = {}  # PRICE (USD/BTC) AT THE ORDER MOMENT
        self._photo_id: dict[int: str] = {}  # ORDER PHOTO ID
        self._cashback: dict[int: int] = {}  # AMOUNT OF CASHBACK

    def update_price(self, user_id: int, prices: dict):
        types = self._type[user_id]
        currency = self._currency[user_id]
        self._price[user_id] = prices['price'] if self._type[user_id] == 1 else prices['usd_price']
        amount = self._amount[user_id] if types == 1 and currency == 1 or types == 2 and currency == 1 else None
        total = self._amount[user_id] if types == 1 and currency == 2 or types == 2 and currency == 2 else None
        rounding = get_round(currency, types)
        if amount is not None:
            self._total[user_id] = round(float(amount) * float(self._price[user_id]), rounding)
            self._amount[user_id] = amount
        elif total is not None:
            self._amount[user_id] = round(float(total) / float(self._price[user_id]), rounding)
            self._total[user_id] = total
        if types == 2:
            if self._network[user_id] == 1:
                self._amount[user_id] = self._amount[user_id] - 1
            else:
                self._amount[user_id] = self._amount[user_id] - 3

    def check_limits(self, user_id: int, limits: dict):
        limit = limits['btc'] if self._type[user_id] == 1 else limits['usd']
        return {
            'result': self._total[user_id] > limit,
            'limit': limit
        }

    def check_min(self, user_id: int, min_values: dict):
        min_value = min_values['btc'] if self._type[user_id] == 1 else min_values['usd']
        return {
            'min': min_value,
            'result': self._total[user_id] < min_value}

    def fresh(self, user_id: int):
        if self._type.get(user_id):
            del self._type[user_id]
        if self._currency.get(user_id):
            del self._currency[user_id]
        if self._network.get(user_id):
            del self._network[user_id]
        if self._amount.get(user_id):
            del self._amount[user_id]
        if self._btc_adr.get(user_id):
            del self._btc_adr[user_id]
        if self._total.get(user_id):
            del self._total[user_id]
        if self._price.get(user_id):
            del self._price[user_id]
        if self._photo_id.get(user_id):
            del self._photo_id[user_id]
        if self._cashback.get(user_id):
            del self._cashback[user_id]

    def get_info(self, user_id: int):
        return {
            'type': self._type.get(user_id),
            'network': self._network.get(user_id),
            'amount': self._amount.get(user_id),
            'address': self._btc_adr.get(user_id),
            'total': self._total.get(user_id),
            'price': self._price.get(user_id),
            'user_id': user_id,
            'currency': self._currency.get(user_id),
            'photo': self._photo_id.get(user_id),
            'cashback': self._cashback.get(user_id)
        }

    def apply_cashback(self, user_id: int, cashback: float):
        self._cashback[user_id] = int(cashback / 3)
        return self._cashback[user_id]

    def set_btc_adr(self, user_id: int, value: float):
        self._btc_adr[user_id] = value

    def set_amount(self, user_id: int, value: float):
        self._amount[user_id] = value

    def get_amount(self, user_id: int):
        return self._amount.get(user_id)

    def set_photo(self, user_id: int, value: str):
        self._photo_id[user_id] = value

    def set_type(self, user_id: int, value: int):
        self._type[user_id] = value

    def get_type(self, user_id: int):
        return self._type.get(user_id)

    def set_network(self, user_id: int, value: int):
        self._network[user_id] = value

    def get_currency_text(self, user_id: int):
        if self._type.get(user_id) == 1:
            types = {
                1: 'BTC',
                2: 'BYN'
            }
        else:
            types = {
                1: 'USD',
                2: 'BYN'
            }
        return types[self._currency.get(user_id)]

    def get_main_currency_text(self, user_id: int):
        return 'BTC' if self._type[user_id] == 1 else 'USD'

    def get_type_text(self, user_id: int):
        if self._type.get(user_id) == 1:
            return 'BTC'
        else:
            if self._network[user_id] == 1:
                return 'TRC-20'
            else:
                return 'ERC-20'

    def set_currency(self, user_id: int, value: int):
        currency_type = 1 if value == 'BTC' or value == 'USD' else 2
        self._currency[user_id] = currency_type


order = Order()


def check_address_by_type(value: str):
    if len(value) > 15:
        return True
    else:
        return False

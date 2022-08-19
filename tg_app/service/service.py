from tg_app.api import update_service_api, get_service_api


class Service:
    def __init__(self):
        self._percent: float = 0.0
        self._usd_percent: float = 0.0
        self._min_btc: int = 0
        self._min_usd: int = 0
        self._btc_limit: int = 0
        self._usd_limit: int = 0
        self._main_photo: str = ''
        self._cashback_percent: float = 0.0
        self._admin_list: dict[int: list[int]] = {}

        self._fetch_data()

    def _fetch_data(self):
        data = get_service_api()
        self._percent = data.percent
        self._usd_percent = data.usd_percent
        self._min_btc = data.min_btc
        self._btc_limit = data.btc_limit
        self._usd_limit = data.usd_limit
        self._main_photo = data.main_photo
        self._min_usd = data.min_usd
        self._cashback_percent = data.cashback_percent

    def update(self, new_data: dict):
        update_service_api(data=new_data)
        return self.refetch()

    def info(self):
        return {
            'percent': self._percent,
            'usd_percent': self._usd_percent,
            'min_btc': self._min_btc,
            'min_usd': self._min_usd,
            'btc_limit': self._btc_limit,
            'usd_limit': self._usd_limit,
            'main_photo': self._main_photo,
            'cashback_percent': self._cashback_percent
        }

    def append_admin_list(self, items, chat_id: int):
        if self._admin_list.get(chat_id) is None:
            self._admin_list[chat_id] = []
        self._admin_list[chat_id].append(items)

    def admin_list(self, chat_id: int):
        items = self._admin_list.get(chat_id)
        if items:
            del self._admin_list[chat_id]
        return items

    @property
    def min_values(self):
        return {
            'btc': self._min_btc,
            'usd': self._min_usd
        }

    @property
    def main_photo(self):
        return self._main_photo

    @property
    def cashback_percent(self):
        return self._cashback_percent

    @property
    def percent(self):
        return self._percent

    @property
    def limits(self):
        return {
            'usd': self._usd_limit,
            'btc': self._btc_limit
        }

    @property
    def usd_percent(self):
        return self._usd_percent

    def refetch(self):
        self._fetch_data()
        return self.info()


service = Service()

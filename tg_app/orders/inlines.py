from telegram import ReplyKeyboardMarkup


def choose_type_inline():
    buttons = [['BTC', 'USDT'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def choose_network_inline():
    buttons = [['TRC-20', 'ERC-20'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def choose_currency(crypto_type: int = 1):
    buttons = [['BTC' if crypto_type == 1 else 'USD', 'BYN'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def choose_cashback_inline():
    buttons = [['Да, использовать', 'Нет'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def confirm_order_inline():
    buttons = [['Подтвердить'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def confirm_pay_inline():
    buttons = [['Оплачено'], ['На главную']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

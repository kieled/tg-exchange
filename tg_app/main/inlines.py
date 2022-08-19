from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def main_inline():
    btn1 = KeyboardButton('Купить BTC/USDT')
    btn2 = KeyboardButton('Актуальные курсы')
    btn3 = KeyboardButton('Бонусы')
    btn4 = KeyboardButton('Мои операции')
    btn5 = KeyboardButton('Поддержка')
    inline = ReplyKeyboardMarkup([
        [btn1],
        [btn2, btn3],
        [btn4, btn5]
    ], resize_keyboard=True)
    return inline


def to_main_inline():
    main = KeyboardButton('На главную')
    inline = ReplyKeyboardMarkup([[main]], resize_keyboard=True)
    return inline


def admin_to_main():
    main = InlineKeyboardButton('На главную', callback_data='admin_to_main')
    inline = InlineKeyboardMarkup([[main]])
    return inline


def support_inline():
    btn = InlineKeyboardButton('Связаться с оператором', url='https://t.me/manetahelp')
    inline = InlineKeyboardMarkup([[btn]])
    return inline

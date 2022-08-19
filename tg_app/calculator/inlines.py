from telegram import KeyboardButton, ReplyKeyboardMarkup


def calc_inline():
    btn1 = KeyboardButton('BYN -> BTC')
    btn2 = KeyboardButton('BTC -> BYN')
    btn3 = KeyboardButton('BYN -> USDT')
    btn4 = KeyboardButton('USDT -> BYN')
    main = KeyboardButton('На главную')
    return ReplyKeyboardMarkup([[btn1, btn2], [btn3, btn4], [main]], resize_keyboard=True, one_time_keyboard=True)

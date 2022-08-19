from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def transfers_inline(page: int = 1, count: int = 0):
    if count <= 3:
        return None
    if page == 1:
        right = InlineKeyboardButton('Вперед ->', callback_data=f'transfers_next,{page + 1}')
        return InlineKeyboardMarkup([[right]])
    elif (3 * page) >= count:
        left = InlineKeyboardButton('<- Назад', callback_data=f'transfers_prev,{page - 1}')
        return InlineKeyboardMarkup([[left]])
    else:
        left = InlineKeyboardButton('<- Назад', callback_data=f'transfers_prev,{page - 1}')
        right = InlineKeyboardButton('Вперед ->', callback_data=f'transfers_next,{page + 1}')
        return InlineKeyboardMarkup([[left, right]])

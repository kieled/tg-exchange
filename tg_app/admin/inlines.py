from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import User, Transaction

btn0 = InlineKeyboardButton('На главную', callback_data='admin_to_main')


def admin_new_order_inline(order_id: int):
    btn1 = InlineKeyboardButton('Подтвердить', callback_data=f'admin_confirm_order,{order_id}')
    btn2 = InlineKeyboardButton('Отменить', callback_data=f'admin_cancel_order,{order_id}')
    btn3 = InlineKeyboardButton('Получить чек', callback_data=f'admin_get_photo,{order_id}')
    inline = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn0]])
    return inline


def admin_menu_inline():
    btn1 = InlineKeyboardButton('Транзакции', callback_data='admin_find,transaction')
    btn2 = InlineKeyboardButton('Пользователи', callback_data='admin_find,user')
    btn3 = InlineKeyboardButton('Настройки', callback_data='admin_settings')
    inline = InlineKeyboardMarkup([[btn1, btn2], [btn3]])
    return inline


def admin_transaction_detail_inline(trans: Transaction):
    btn1 = InlineKeyboardButton('Чек', callback_data=f'admin_get_photo,{trans.id}')
    btn2 = InlineKeyboardButton('О пользователе', callback_data=f'admin_get_user,{trans.user_id}')
    btn3 = InlineKeyboardButton('Изменить статус', callback_data=f'admin_transaction_status,{trans.id}')
    inline = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn0]])
    return inline


def admin_user_detail_inline(user: User):
    btn1 = InlineKeyboardButton('Разблокировать' if user.is_banned else 'Заблокировать',
                                callback_data=f'admin_block_user,{user.id}')
    inline = InlineKeyboardMarkup([[btn1, btn0]])
    return inline


def admin_transaction_status_inline(trans_id: int):
    btn1 = InlineKeyboardButton('Завершён', callback_data=f'admin_confirm_order,{trans_id}')
    btn2 = InlineKeyboardButton('В обработке', callback_data=f'admin_transaction_status,{trans_id},2')
    btn3 = InlineKeyboardButton('Отменён', callback_data=f'admin_cancel_order,{trans_id}')
    inline = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn0]])
    return inline


def settings_list_inline():
    btn1 = InlineKeyboardButton('Наценка BTC', callback_data='admin_setting,1')
    btn2 = InlineKeyboardButton('Наценка USDT', callback_data='admin_setting,2')
    btn3 = InlineKeyboardButton('Минималка BTC', callback_data='admin_setting,3')
    btn5 = InlineKeyboardButton('Минималка USD', callback_data='admin_setting,4')
    btn6 = InlineKeyboardButton('Бонус %', callback_data='admin_setting,5')
    btn7 = InlineKeyboardButton('Объем BTC', callback_data='admin_setting,6')
    btn8 = InlineKeyboardButton('Объем USD', callback_data='admin_setting,7')
    btn9 = InlineKeyboardButton('Изменить баннер', callback_data='admin_setting,8')
    inline = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn5], [btn6, btn7], [btn8, btn9], [btn0]])
    return inline


def to_main_with_settings():
    btn = InlineKeyboardButton('Вернуться к настройкам', callback_data='admin_settings')
    inline = InlineKeyboardMarkup([[btn, btn0]])
    return inline


def admin_delete_msg_inline():
    btn = InlineKeyboardButton('Закрыть', callback_data='admin_delete_msg')
    inline = InlineKeyboardMarkup([[btn]])
    return inline

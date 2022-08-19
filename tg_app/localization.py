from database.models import Requisites, User, Transaction

welcome_message = 'Добро пожаловать в МАНЕТА Exсhange. У нас вы можете приобрести BTC/USDT за белорусские ' \
                  'рубли через ЕРИП.'

not_understand = 'Ошибка, проверьте правильность ввода'

empty_transactions = 'Вы еще не совершали обменов...'

invalid_number_message = 'Введена неверная сумма. Попробуйте еще раз.'

invalid_address_message = 'Введен неверный адрес, попробуйте еще раз.'

choose_type_order_message = 'Выберите криптовалюту, которую хотите приобрести.'

choose_network_order_message = 'Выберите сеть USDT, для кошелька, на который вы будете получать средства'

success_order_message = 'Ваша заявка успешно создана. Когда она будет обработана, вам прийдет уведомление (обычно это ' \
                        'заниает от 1 до 30 минут в рабочее время). Также вы ' \
                        'можете отследить её статус переходя в пункт "Мои операции" '

send_photo_message = 'Отправьте пожалуйста чек (изображение, не путать с документом!)'

admin_pass_link_message = 'Вставьте ссылку на транзакцию'

admin_menu_message = 'Панель управления для админов.'

admin_send_id_message = 'Введите ID транзакции'

admin_send_id_or_username_message = 'Введите ID или имя пользователя'

admin_invalid_id_message = 'Вы ввели неверный ID. Попробуйте ещё раз'

invalid_value_message = 'Неверное значение, попробуйте ещё раз.'

not_found = 'Не найдено. Попробуйте еще раз'

admin_settings_text_message = 'Выберите нужный пункт'

admin_invalid_value = 'Вы отправили неверное значение. Попробуйте снова'

admin_saved_changes = 'Изменения успешно сохранены'

support_message = 'Время работы поддержки: 10:00 - 00:00'
# support_message = 'Бот находиться на тех.работах. В случае возникновения вопросов, просьба обратиться в поддержку.'

admin_response_setting_message = [
    'Введите нужный курс для BTC',
    'Введите нужный курс для USDT',
    'Введите кол-во BYN, которых будет необходимо для создания сделки BTC',
    'Введите кол-во BYN, которых будет необходимо для создания сделки USDT',
    'Введите процент, в формате 0.01 (1%)',
    'Введите сумму в BYN, которой вы на данный момент обладаете для продажи BTC',
    'Введите сумму в BYN, которой вы на данный момент обладаете для продажи USDT',
    'Отправьте новое изображение',
]


def admin_order_confirmed_success_message(id: int):
    return f'Заявка #{id} успешно подтверждена'


def admin_order_cancel_message(id: int):
    return f'Заявка #{id} была отклонена'


def admin_setting_info_message(choice: int, info: dict):
    message = ''
    if choice != 8:
        message += f'Текущее значение: {str(info[str_by_choice(choice)])}\n'
    message += admin_response_setting_message[choice - 1]
    return message


def order_amount_limit(amount: float):
    return f'На данный момент существует лимит в {amount} BYN. Попробуйте еще раз, ' \
           f'указав значение ниже. '


def order_cashback_choice_message(count: float):
    return f'Жалаете использовать бонусы?\n\nБонусный баланс: {int(count)} BYN\n\n---\n\nПри подтверждении будет ' \
           f'списано 30% от суммы бонусов. '


def user_complete_order_message(trans_id: int, link: str):
    return f'Ваша заявка #{trans_id} была успешно обработана. \nСсылка на транзакцию: {link}'


def user_cancel_order_message(trans_id: int):
    return f'Ваша заявка #{trans_id} была отклонена. Если вы считаете, что произошла ошибка, просьба обратиться к ' \
           f'нашему оператору, для этого нужно в главном меню выбрать "Поддержка" '


def input_value_adr_message(text: str):
    return f'Введите адрес {text} на который нужно отправить средства'


def choose_currency_message(text: str):
    return 'Выберите валюту, в которой вы будете указывать сумму сделки. В процессе создания сделки, ' \
           f'сумма будет автоматически конвертирована в {text}'


def min_price_message(value: float):
    return f'Минимальная сумма для создания заявки {value} BYN (если вы указываете сумму в BTC либо USDT, тогда она ' \
           f'автоматически конвертируются в BYN и проверяетя. Попробуйте ещё раз. '


def calculator_result(value: float, currency: str):
    return f'Вы получите {value} {currency}'


def input_value_message(currency: str):
    return f'Введите сумму в {currency}'


def calculator_price(price: dict):
    return 'Актуальные курсы:\n\n' + \
           f'1 BTC = {price["price"]} BYN\n' + \
           f'1 USDT = {price["usd_price"]} BYN\n\n' + \
           'Для конвертации выберите нужное направление ниже'


def cashback_message(amount: float):
    return f'Сумма бонусного баланса составляет: {int(amount)} BYN'


def changed_status_trans(trans_id: int, status: int):
    lst = ['Завершен', 'В обработе', 'Отменен']
    return f'Статус вашей сделки #{trans_id} изменён на "{lst[status - 1]}"'


def trans_list_message(items: list[Transaction]):
    if len(items) == 0:
        return empty_transactions
    message = add_stars()
    status = ['Завершен', 'В обработе', 'Отменен']
    for item in items:
        message += f'ID: {item.id}\n'
        message += f'Дата: {item.date_created}\n'
        message += f'Сумма: {item.amount} {"BTC" if item.type == 1 else "USD"}\n'
        message += f'Курс обмена: {item.price} BYN\n'
        message += f'Статус: {status[int(item.status) - 1]}\n\n'
        message = add_stars(message)
    return message


def admin_trans_detail_message(item: Transaction):
    status = ['Завершен', 'В обработе', 'Отменен']

    message = f'ID: `{item.id}`\n'
    message += f'Дата: {item.date_created}\n'
    message += f'Сумма: `{item.amount}` {"BTC" if item.type == 1 else "USDT"}\n'
    message += f'Курс обмена: {item.price} {"BTC" if item.type == 1 else "USD"}\n'
    if item.type == 2:
        message += f'Сеть: {"TRC-20" if item.network == 1 else "ERC-20"}\n'
    message += f'Полученная сумма: {item.total} BYN\n'
    message += f'Статус: {status[int(item.status) - 1]}\n\n'
    message += f'Кошелек получателя: `{item.address}`'
    return message


def admin_user_detail_message(item: User):
    message = f'ID: {item.id}\n'
    message += f'Username: @{item.username}\n'
    message += f'Кол-во сделок: {item.count_trades}\n'
    message += f'Общая сумма сделок: {item.sum_trades} BYN\n'
    message += f'Кэшбек: {round(item.cashback, 1)} BYN\n'
    message += f'Дата регистрации: {item.date_created}'
    return message


def get_total_order_info_message(data: dict):
    currency = "BTC" if data['type'] == 1 else "USDT"
    message = add_stars()
    coms_message = f' c учётом комиссии сети {"3 USDT" if data["network"] == 2 else "1 USDT"}' if data["type"] == 2 else ''
    if data['cashback']:
        message += f'Сумма {data["amount"]} {currency}{coms_message} ({int(data["total"] - data["cashback"])} BYN с ' \
                   f'учётом бонуса {int(data["cashback"])} BYN) \n '
    else:
        message += f'Сумма: {data["amount"]} {currency}{coms_message} ({data["total"]} BYN)\n '
    message += f'Адрес вашего кошелька: {data["address"]}\n'
    if data['type'] == 2:
        message += f'Сеть: {"TRC-20" if data["network"] == 1 else "ERC-20"}\n'
    message += f'Курс обмена: {data["price"]} {"BYN" if data["type"] == 1 else "USD"}\n\n'
    message = add_stars(message)
    return message


def add_stars(message: str = ''):
    return message + '**************************************\n'


def requisites_message(order: dict, data: Requisites):
    message = add_stars()
    message += f'Для оплаты используйте указанные ниже реквизиты. Нажмите для копирования\n\n`{data.data}`\n\n'
    message += f'Как оплатить: {data.info}\n\n'
    if order['cashback'] and order['cashback'] > 0:
        message += f'Сумма к оплате: {int(order["total"] - order["cashback"])} BYN\n\n'
    else:
        message += f'Сумма к оплате: {order["total"]} BYN\n\n'
    message = add_stars(message)
    message += 'Внимание! После оплаты не забудьте сохранить чек - Обязательно'
    return message


def admin_new_order_message(order: Transaction):
    currency = "BTC" if order.type == 1 else "USDT"
    message = f'Новая заявка #{order.id}\n'
    message += f'Пользователь покупает {currency}\n'
    message += f'Сумма: {order.total} BYN\n'
    if order.type == 2:
        message += f'Сеть: {"TRC-20" if order.network == 1 else "ERC-20"}\n'
    message += f'Кошелек пользователя: `{order.address}`\n'
    message += f'Сумма к переводу: `{order.amount}` {currency}'
    return message


def str_by_choice(choice: int):
    if choice == 1:
        return 'percent'
    if choice == 2:
        return 'usd_percent'
    if choice == 3:
        return 'min_btc'
    if choice == 4:
        return 'min_usd'
    if choice == 5:
        return 'cashback_percent'
    if choice == 6:
        return 'btc_limit'
    if choice == 7:
        return 'usd_limit'
    if choice == 8:
        return 'main_photo'

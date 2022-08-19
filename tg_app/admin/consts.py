def value_by_choice(choice: int, value: str | int | float) -> dict:
    return {str_by_choice(choice): get_percent(choice, value)}


def get_percent(choice: int, value: int | float | str):
    return value


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


def value_validate_by_choice(choice: int, message: any):
    integers = [1, 3, 4, 6, 7]
    floats = [2, 5]
    try:
        if choice in integers:
            return int(message.text)
        if choice in floats:
            return float(message.text)
        else:
            return message.photo[-1].file_id
    except:
        return None

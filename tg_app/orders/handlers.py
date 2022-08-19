from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from tg_app.admin.inlines import admin_new_order_inline
from tg_app.api import get_requisites, create_order_api, get_admins, get_user_info, admin_get_transaction
from tg_app.calculator.calculator import calculator
from tg_app.localization import choose_currency_message, input_value_message, min_price_message, \
    input_value_adr_message, get_total_order_info_message, requisites_message, \
    choose_type_order_message, choose_network_order_message, success_order_message, admin_new_order_message, \
    send_photo_message, order_amount_limit, invalid_address_message, order_cashback_choice_message
from tg_app.main.inlines import to_main_inline
from tg_app.orders.inlines import confirm_order_inline, confirm_pay_inline, choose_type_inline, choose_network_inline, \
    choose_currency, choose_cashback_inline
from tg_app.orders.order import order, check_address_by_type
from tg_app.service.service import service
from tg_app.consts import *


async def order_type_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_type_order_message, reply_markup=choose_type_inline())
    return TYPE


async def order_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat.id
    order_type = 1 if update.message.text == 'BTC' else 2
    order.set_type(user, order_type)
    return await order_currency_choose(update, context) if order_type == 1 else await order_network_choose(update,
                                                                                                           context)


async def order_network_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_network_order_message,
                                    reply_markup=choose_network_inline())
    return NETWORK


async def order_network_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    network_type = 1 if update.message.text == 'TRC-20' else 2
    order.set_network(update.effective_chat.id, network_type)
    return await order_currency_choose(update, context)


async def order_currency_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_currency_message(order.get_main_currency_text(update.effective_chat.id)),
                                    reply_markup=choose_currency(order.get_type(update.effective_chat.id)))
    return CURRENCY


async def order_currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order.set_currency(update.effective_chat.id, update.message.text)
    return await order_input_choose(update, context)


async def order_input_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = order.get_currency_text(update.effective_chat.id)
    await update.message.reply_text(input_value_message(text), reply_markup=to_main_inline())
    calculator.get_price()
    return AMOUNT


async def order_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        float(update.message.text)
    except ValueError:
        return AMOUNT
    order.set_amount(update.effective_chat.id, float(update.message.text))
    order.update_price(update.effective_chat.id, calculator.get_price())
    data = order.check_limits(update.effective_chat.id, service.limits)
    if data['result']:
        await update.message.reply_text(order_amount_limit(float(data['limit'])))
        return AMOUNT
    data = order.check_min(update.effective_chat.id, service.min_values)
    if data['result']:
        await update.message.reply_text(min_price_message(data['min']))
        return AMOUNT
    return await order_btc_adr_choose(update, context)


async def order_btc_adr_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_type = order.get_type_text(update.effective_chat.id)
    await update.message.reply_text(input_value_adr_message(wallet_type), reply_markup=to_main_inline())
    return ADDRESS


async def order_btc_adr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and check_address_by_type(update.message.text):
        order.set_btc_adr(update.effective_chat.id, update.message.text)
    else:
        await update.message.reply_text(invalid_address_message, reply_markup=to_main_inline())
        return ADDRESS
    return await order_cashback_choose(update, context)


async def order_cashback_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_info(update.effective_chat.id)
    if int(user.cashback) < 3:
        return await order_complete_choose(update, context)
    await update.message.reply_text(order_cashback_choice_message(user.cashback),
                                    reply_markup=choose_cashback_inline())
    return CASHBACK


async def order_cashback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_info(update.effective_chat.id)

    if update.message.text == 'Да, использовать':
        order.apply_cashback(update.effective_chat.id, float(user.cashback))

    return await order_complete_choose(update, context)


async def order_complete_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = order.get_info(update.effective_chat.id)
    await update.message.reply_text(get_total_order_info_message(info),
                                    reply_markup=confirm_order_inline())
    return CONFIRM


async def confirmed_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instance = order.get_info(update.effective_chat.id)
    requisites = get_requisites()
    await update.message.reply_markdown(requisites_message(instance, requisites),
                                        reply_markup=confirm_pay_inline())
    return CONFIRMED


async def order_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await order_get_photo_choose(update, context)


async def order_get_photo_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(send_photo_message, reply_markup=to_main_inline())
    return CREATE


async def create_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        order.set_photo(update.effective_chat.id, update.message.photo[-1].file_id)
        order_id = create_order_api(order.get_info(update.effective_chat.id))
        order.fresh(update.effective_chat.id)
        await update.message.reply_text(success_order_message, reply_markup=to_main_inline())
        admins = get_admins()
        item = admin_get_transaction(transaction_id=order_id)
        for admin in admins:
            msg = await update.message.get_bot().send_message(admin, admin_new_order_message(item),
                                                              reply_markup=admin_new_order_inline(item.id),
                                                              parse_mode='Markdown')
            service.append_admin_list([admin, msg.id], update.effective_chat.id)
        return ConversationHandler.END
    else:
        await update.message.reply_text(send_photo_message)
        return CREATE

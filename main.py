from dataclasses import dataclass

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from telegram import Update
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, \
    CallbackQueryHandler, CallbackContext, ExtBot, Application
import uvicorn
from tg_app.admin.handlers import admin_confirm_order_choose, admin_confirm_order_handler, admin_cancel_order_handler, \
    admin_get_photo_handler, admin_find_choose, admin_find_handler, admin_select_choice, admin_select_handler, \
    admin_get_user_handler, admin_block_user_handler, admin_transaction_status_handler, admin_settings_handler, \
    admin_close_message
from tg_app.api import get_cashback_info
from tg_app.calculator.handlers import calculator_handle, calculator_handler, calculate
from tg_app.consts import *
from tg_app.localization import support_message, cashback_message, not_understand
from tg_app.main.handlers import start_handler, to_main_handler
from tg_app.main.inlines import support_inline
from tg_app.orders.handlers import order_type_choose, order_type_handler, order_input_handler, \
    order_currency_handler, order_network_handler, order_btc_adr_handler, order_cashback_handler, \
    confirmed_order_handler, create_order_handler, order_confirm_handler
from tg_app.transfers.handlers import transfer_list_choose, transfer_list


TG_TOKEN = 'YOUR TG TOKEN'


def callback_func(objects: list[str]):
    def wrapper(data: object) -> bool:
        return str(data).split(',')[0] in objects

    return wrapper


WEBHOOK_URL_BASE = "https://example.com"
WEBHOOK_URL_PATH = "/{}/".format(TG_TOKEN)

text_with_out = filters.TEXT & ~ filters.Text(['На главную', 'Отменить'])
fallback = [MessageHandler(filters.Text(['На главную', 'Отменить']), to_main_handler)]


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(support_message, reply_markup=support_inline())


async def cashback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_cashback_info(update.effective_chat.id)
    await update.message.reply_text(cashback_message(data))


async def not_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(not_understand)


async def admin_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await to_main_handler(update, context)


def gen_conv(f1, t1: list[str], f2, c: int):
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(f1, callback_func(t1))],
        states={
            c: [MessageHandler(text_with_out, f2)]
        },
        fallbacks=fallback,
        allow_reentry=True
    )


async def main():
    bot = Application.builder().token(TG_TOKEN).build()
    await bot.bot.set_webhook(url=WEBHOOK_URL_BASE + '/hook/')

    order_calc = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(['Купить BTC/USDT']), order_type_choose)],
        states={
            TYPE: [MessageHandler(filters.Text(['BTC', 'USDT']), order_type_handler)],
            NETWORK: [MessageHandler(filters.Text(['TRC-20', 'ERC-20']), order_network_handler)],
            CURRENCY: [MessageHandler(filters.Text(['BTC', 'USD', 'BYN']), order_currency_handler)],
            AMOUNT: [MessageHandler(text_with_out, order_input_handler)],
            ADDRESS: [MessageHandler(text_with_out, order_btc_adr_handler)],
            CASHBACK: [MessageHandler(text_with_out, order_cashback_handler)],
            CONFIRM: [MessageHandler(filters.Text(['Подтвердить']), confirmed_order_handler)],
            CONFIRMED: [MessageHandler(filters.Text(['Оплачено']), order_confirm_handler)],
            CREATE: [MessageHandler(filters.ALL & ~ filters.Text(['На главную', 'Отменить']), create_order_handler)]

        },
        fallbacks=fallback,
        allow_reentry=True
    )

    calculator_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(['Актуальные курсы']), calculator_handle)],
        states={
            CHOOSE_CALC: [MessageHandler(filters.Text(['BYN -> BTC', 'BTC -> BYN', 'BYN -> USDT', 'USDT -> BYN']),
                                         calculator_handler)],
            CALCULATE: [MessageHandler(text_with_out, calculate)]
        },
        fallbacks=fallback,
        allow_reentry=True
    )

    admin_confirm_conv = gen_conv(admin_confirm_order_choose, ['admin_confirm_order'], admin_confirm_order_handler,
                                  ADMIN_LINK)

    admin_find_conv = gen_conv(admin_find_choose, ['admin_find'], admin_find_handler, ADMIN_FIND)

    admin_setting_conv = gen_conv(admin_select_choice, ['admin_setting'], admin_select_handler, ADMIN_SETTING)

    bot.add_handler(order_calc)
    bot.add_handler(calculator_conv)
    bot.add_handler(admin_confirm_conv)
    bot.add_handler(admin_find_conv)
    bot.add_handler(admin_setting_conv)

    bot.add_handlers([
        CommandHandler("start", start_handler),
        MessageHandler(filters.Text(['На главную']), start_handler)
    ])
    bot.add_handler(MessageHandler(filters.Text(['Поддержка']), support_handler))
    bot.add_handler(MessageHandler(filters.Text(['Бонусы']), cashback_handler))
    bot.add_handler(MessageHandler(filters.Text(['Мои операции']), transfer_list_choose))

    bot.add_handlers(
        [
            CallbackQueryHandler(transfer_list, callback_func(['transfers_prev', 'transfers_next'])),
            CallbackQueryHandler(admin_to_main, callback_func(['admin_to_main'])),
            CallbackQueryHandler(admin_cancel_order_handler, callback_func(['admin_cancel_order'])),
            CallbackQueryHandler(admin_get_photo_handler, callback_func(['admin_get_photo'])),
            CallbackQueryHandler(admin_get_user_handler, callback_func(['admin_get_user'])),
            CallbackQueryHandler(admin_block_user_handler, callback_func(['admin_block_user'])),
            CallbackQueryHandler(admin_transaction_status_handler, callback_func(['admin_transaction_status'])),
            CallbackQueryHandler(admin_settings_handler, callback_func(['admin_settings'])),
            CallbackQueryHandler(admin_close_message, callback_func(['admin_delete_msg'])),
        ]
    )
    bot.add_handler(MessageHandler(filters.TEXT, not_found))

    app = FastAPI(docs_url=None, redoc_url=None)

    @app.post('/hook/')
    async def process_webhook(request: Request) -> Response:
        await bot.update_queue.put(
            Update.de_json(data=await request.json(), bot=bot.bot)
        )
        return Response()

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8443,
            host="0.0.0.0",
            proxy_headers=True
        )
    )

    async with bot:
        await bot.start()
        await webserver.serve()
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())

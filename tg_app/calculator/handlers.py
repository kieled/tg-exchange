from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from tg_app.calculator.calculator import calculator
from tg_app.calculator.inlines import calc_inline
from tg_app.consts import CALCULATE, CHOOSE_CALC
from tg_app.localization import invalid_number_message, calculator_price, input_value_message
from tg_app.main.inlines import to_main_inline, main_inline


async def calculator_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def send_message(value: int, text: str):
        chat_id = update.effective_chat.id
        calculator.set(value, chat_id)
        await update.message.reply_text(input_value_message(text), reply_markup=to_main_inline())

    value = update.message.text

    if value == 'BTC -> BYN':
        await send_message(1, 'BTC')
    if value == 'BYN -> BTC':
        await send_message(2, 'BYN')
    if value == 'USDT -> BYN':
        await send_message(3, 'USDT')
    if value == 'BYN -> USDT':
        await send_message(4, 'BYN')

    return CALCULATE


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = calculator.calculate(update.effective_chat.id, float(update.message.text))
        await update.message.reply_text(data, reply_markup=main_inline())
        return ConversationHandler.END
    except:
        await update.message.reply_text(invalid_number_message, reply_markup=to_main_inline())
        return CALCULATE


async def calculator_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(calculator_price(calculator.get_price()),
                                    reply_markup=calc_inline())
    return CHOOSE_CALC

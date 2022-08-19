from telegram import Update
from telegram.ext import ContextTypes

from tg_app.api import get_user_transactions
from tg_app.localization import trans_list_message
from tg_app.transfers.inlines import transfers_inline


def indexExists(list, index):
    if 0 <= index < len(list):
        return True
    else:
        return False


async def transfer_list_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_user_transactions(update.effective_chat.id)
    inline = transfers_inline(1, items.get('count'))
    await update.message.reply_text(trans_list_message(items.get('result')), reply_markup=inline)


async def transfer_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_user_transactions(update.effective_chat.id, int(update.callback_query.data.split(",")[1]))
    inline = transfers_inline(int(update.callback_query.data.split(',')[1]), items.get('count'))
    await update.callback_query.message.edit_text(trans_list_message(items.get('result')), reply_markup=inline)
    await update.callback_query.answer()

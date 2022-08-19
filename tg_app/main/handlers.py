from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.schemas import UserIn
from tg_app.admin.inlines import admin_menu_inline
from tg_app.api import get_user_info, create_user
from tg_app.calculator.calculator import calculator
from tg_app.localization import welcome_message, admin_menu_message
from tg_app.main.inlines import main_inline
from tg_app.orders.order import order
from tg_app.service.service import service


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        order.fresh(chat_id)
        calculator.clear(chat_id)
    except:
        pass
    user = get_user_info(chat_id)
    if not user:
        data = UserIn(chat_id=chat_id, username=update.effective_user.username)
        user = create_user(data)
    if user.is_admin:
        await update.message.reply_text(admin_menu_message, reply_markup=admin_menu_inline())
        await update.message.delete()
    else:
        if service.main_photo:
            await update.message.reply_photo(service.main_photo)
        await update.message.reply_text(welcome_message, reply_markup=main_inline())


async def to_main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    chat_id = update.effective_chat.id
    user = get_user_info(chat_id)
    if user.is_admin:
        return await update.callback_query.message.edit_text(admin_menu_message, reply_markup=admin_menu_inline())
    order.fresh(chat_id)
    calculator.clear(chat_id)
    if service.main_photo:
        await update.message.reply_photo(service.main_photo)
    await update.message.reply_text(welcome_message, reply_markup=main_inline())
    return ConversationHandler.END

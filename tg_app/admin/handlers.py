from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from tg_app.admin.consts import value_validate_by_choice, value_by_choice
from tg_app.admin.inlines import admin_transaction_detail_inline, admin_user_detail_inline, \
    admin_transaction_status_inline, settings_list_inline, to_main_with_settings, admin_delete_msg_inline
from tg_app.api import complete_transaction, cancel_transaction, admin_get_transaction, \
    admin_block_user, \
    admin_change_status, admin_get_user_by_id, admin_get_user_by_username
from tg_app.consts import ADMIN_LINK, ADMIN_FIND, ADMIN_SETTING
from tg_app.localization import admin_pass_link_message, \
    user_complete_order_message, user_cancel_order_message, admin_send_id_message, \
    admin_invalid_id_message, admin_trans_detail_message, not_found, admin_user_detail_message, \
    admin_settings_text_message, admin_invalid_value, admin_saved_changes, \
    admin_setting_info_message, admin_send_id_or_username_message
from tg_app.main.inlines import admin_to_main
from tg_app.service.service import service


async def admin_close_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.callback_query.message.delete()
    except:
        pass


async def admin_confirm_order_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    msg = await update.callback_query.message.reply_text(admin_pass_link_message)
    context.user_data.update(trans_id=int(update.callback_query.data.split(',')[1]), msg=msg.id)
    return ADMIN_LINK


async def admin_confirm_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trans_id = context.user_data.get('trans_id')
    msg_id = context.user_data.get('msg')
    complete_transaction(transaction_id=trans_id)
    info = admin_get_transaction(transaction_id=trans_id)
    chat_id = admin_get_user_by_id(info.user_id).chat_id
    if context.user_data.get('update'):
        for item in service.admin_list(chat_id):
            try:
                await update.message.get_bot().delete_message(item[0], item[1])
            except:
                pass
        context.user_data.clear()
    else:
        context.user_data.clear()
    try:
        await update.message.get_bot().delete_message(update.effective_chat.id, msg_id)
    except:
        pass
    try:
        await update.message.get_bot().send_message(chat_id, user_complete_order_message(trans_id, update.message.text))
    except:
        pass
    try:
        await update.message.delete()
    except:
        pass
    return ConversationHandler.END


async def admin_cancel_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trans_id = int(update.callback_query.data.split(',')[1])
    info = admin_get_transaction(transaction_id=trans_id)
    chat_id = admin_get_user_by_id(info.user_id).chat_id
    for item in service.admin_list(chat_id):
        try:
            await update.callback_query.get_bot().delete_message(item[0], item[1])
        except:
            pass
    try:
        await update.callback_query.message.delete()
    except:
        pass
    cancel_transaction(transaction_id=trans_id)
    info = admin_get_transaction(transaction_id=trans_id)
    chat_id = admin_get_user_by_id(info.user_id).chat_id

    try:
        await update.callback_query.get_bot().send_message(chat_id, user_cancel_order_message(trans_id))
    except:
        pass


async def admin_get_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    trans_id = int(update.callback_query.data.split(',')[1])
    info = admin_get_transaction(transaction_id=trans_id)
    await update.callback_query.message.reply_photo(info.photo, reply_markup=admin_delete_msg_inline())


async def admin_find_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    find_type = 1 if update.callback_query.data.split(',')[1] == 'transaction' else 2
    message = admin_send_id_message if find_type == 1 else admin_send_id_or_username_message
    await update.callback_query.message.edit_text(message, reply_markup=admin_to_main())
    context.user_data.update(find_type=find_type, msg=update.callback_query.message.id)
    await update.callback_query.answer()
    return ADMIN_FIND


async def admin_find_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.get_bot().delete_message(update.effective_chat.id, context.user_data.get('msg'))
    except:
        pass
    try:
        await update.message.delete()
    except:
        pass


async def admin_find_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    find_type = context.user_data.get('find_type')
    if find_type == 1:
        try:
            int(text)
        except:
            msg = await update.message.reply_text(admin_invalid_id_message, reply_markup=admin_to_main())
            await admin_find_delete(update, context)
            context.user_data.update(msg=msg.id)
            return ADMIN_FIND
        item = admin_get_transaction(transaction_id=int(text))
        if item:
            msg = admin_trans_detail_message(item)
        else:
            msg = None
    else:
        try:
            int(text)
            item = admin_get_user_by_id(user_id=int(text))
        except:
            item = admin_get_user_by_username(username=text)
        if item:
            msg = admin_user_detail_message(item)
        else:
            msg = None
    if msg:
        if find_type == 1:
            markup = admin_transaction_detail_inline(item)
        else:
            markup = admin_user_detail_inline(item)
        await update.message.reply_markdown(msg, reply_markup=markup)
        await admin_find_delete(update, context)
        context.user_data.clear()
        return ConversationHandler.END
    else:
        msg = await update.message.reply_text(not_found, reply_markup=admin_to_main())
        await admin_find_delete(update, context)
        context.user_data.update(msg=msg.id)
        return ADMIN_FIND


async def admin_get_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = int(update.callback_query.data.split(',')[1])
    item = admin_get_user_by_id(user_id=data)
    await update.callback_query.message.edit_text(admin_user_detail_message(item),
                                                  reply_markup=admin_user_detail_inline(item))
    await update.callback_query.answer()


async def admin_block_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = int(update.callback_query.data.split(',')[1])
    admin_block_user(user_id=data)
    item = admin_get_user_by_id(user_id=data)
    await update.callback_query.message.edit_text(admin_user_detail_message(item),
                                                  reply_markup=admin_user_detail_inline(item))
    await update.callback_query.answer()


async def admin_transaction_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data.split(',')
    if len(data) == 3:
        admin_change_status(trans_id=int(data[1]))
        trans = admin_get_transaction(transaction_id=int(data[1]))
        await update.callback_query.message.edit_text(admin_trans_detail_message(trans),
                                                      parse_mode='Markdown',
                                                      reply_markup=admin_transaction_detail_inline(trans))
    else:
        await update.callback_query.message.edit_text('Выберите статус',
                                                      reply_markup=admin_transaction_status_inline(int(data[1])))
        context.user_data.update(custom=True)
    await update.callback_query.answer()


async def admin_settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(admin_settings_text_message, reply_markup=settings_list_inline())
    await update.callback_query.answer()


async def admin_select_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = int(update.callback_query.data.split(',')[1])
    context.user_data.update(choice=choice, msg=update.callback_query.message.id)
    text = admin_setting_info_message(choice, service.info())
    await update.callback_query.message.edit_text(text, reply_markup=admin_to_main())
    await update.callback_query.answer()
    return ADMIN_SETTING


async def admin_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = value_validate_by_choice(context.user_data.get('choice'), update.message)
    if value is None:
        await update.message.reply_text(admin_invalid_value)
        return ADMIN_SETTING
    service.update(value_by_choice(context.user_data.get('choice'), value))
    await update.message.reply_text(admin_saved_changes, reply_markup=to_main_with_settings())
    await admin_find_delete(update, context)
    return ConversationHandler.END

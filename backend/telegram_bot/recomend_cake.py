from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater
)

from .db_querrys import (
    get_random_preset_cake
)

from .start import start


def recomend_cake(update: Update, context: CallbackContext):
    cake = get_random_preset_cake()
    show_cake(update, context, cake)

def unshow_recomend_cake_start(update, context):
    query = update.callback_query
    query.answer()    
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    start(update, context)

def show_cake(update: Update, context: CallbackContext, cake: dict):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    # Удаляем старое сообщение
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    # Отправляем новое сообщение с изображением, описанием и кнопками
    image_url = cake.image.name
    caption = f"""Торт {cake.title}
Количество уровней: {cake.level.title}
Форма: {cake.form.title}
Топинг: {cake.topping.title}
Ягода: {cake.berry.title}
Декор: {cake.decor.title}

Цена: {cake.price} рублей
"""
    context.user_data['recomend_cake'] = cake

    # Определяем кнопки
    keyboard = [    
        [InlineKeyboardButton("Заказать", callback_data='get_data_for_cake')],
        [InlineKeyboardButton("Назад", callback_data='unshow_recomend_cake_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем новое сообщение с изображением и кнопками
    context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        reply_markup=reply_markup
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(recomend_cake, pattern="^recomend_cake$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(unshow_recomend_cake_start, pattern="^unshow_recomend_cake_start$")
    )
    return updater.dispatcher
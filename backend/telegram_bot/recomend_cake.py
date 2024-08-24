from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater
)


import pdb

from .db_querrys import (
    get_random_preset_cake
)


def recomend_cake(update: Update, context: CallbackContext):
    cake = get_random_preset_cake()
    show_cake(update, context, "start", "v", cake)

def unshow_cake(update, context):
    query = update.callback_query
    query.answer()    
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    context.bot.send_message('')
    update.callback_query = context.user_data['cake_showed_back_step']
    context.user_data['cake_showed_back_step'] = None


def show_cake(update: Update, context: CallbackContext,
              back_step_callback: str, next_step_callback: str, cake: dict):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.user_data['cake_showed_back_step'] = back_step_callback
    context.user_data['cake_showed_back_step'] = next_step_callback
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


    # Определяем кнопки
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data='unshow_cake'),],
        [InlineKeyboardButton("Выбрать", callback_data='unshow_cake')]
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
        CallbackQueryHandler(unshow_cake, pattern="^unshow_cake$")
    )
    return updater.dispatcher

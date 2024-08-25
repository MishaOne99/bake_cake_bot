from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

from .common_functions import build_button_table
from .db_querrys import get_cake, get_presets_cakes


def list_cakes(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    cakes = get_presets_cakes()

    buttons = [
        InlineKeyboardButton(
            cake.title,
            callback_data=f"cake_id_{cake.id}",
        )
        for cake in cakes
    ]
    back_button = [InlineKeyboardButton("Назад", callback_data='start')]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(back_button)
    buttons_markup = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_text(
            text="Готовые торты:",
            reply_markup=buttons_markup,
        )
    except(Exception):
        context.bot.send_message(
            text="Готовые торты:",
            reply_markup=buttons_markup,
            chat_id=update.effective_chat.id
        )


def unshow_cake_list_cakes(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    list_cakes(update, context)

def show_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if not context.user_data.get("cake_id"):
        context.user_data["cake_id"] = query.data.split("_")[-1]
    cake = get_cake(context.user_data["cake_id"])

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
    context.user_data['preset_cake'] = cake
    # Определяем кнопки
    keyboard = [        
        [InlineKeyboardButton("Заказать", callback_data="get_data_for_cake")],
        [
            InlineKeyboardButton(
                "Назад",
                callback_data='unshow_cake_list_cakes',
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем новое сообщение с изображением и кнопками
    context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        reply_markup=reply_markup,
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(list_cakes, pattern="^list_cakes$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(show_cake, pattern="^cake_id_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(unshow_cake_list_cakes, pattern="^unshow_cake_list_cakes$")
    )
    return updater.dispatcher

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

from .common_functions import build_button_table
from .db_querrys import get_cake, get_presets_cakes, get_random_preset_cake
from .start import start

from django.conf import settings

def list_cakes(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["back_step"] = "list_cakes"
    cakes = get_presets_cakes()

    buttons = [
        InlineKeyboardButton(
            cake.title,
            callback_data=f"cake_id_{cake.id}",
        )
        for cake in cakes
    ]
    back_button = [InlineKeyboardButton("Назад", callback_data="start")]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(back_button)
    keyboard = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_text(
            text="Готовые торты:",
            reply_markup=keyboard,
        )
    except Exception:
        context.bot.send_message(
            text="Готовые торты:",
            reply_markup=keyboard,
            chat_id=update.effective_chat.id,
        )


def recomend_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    cake = get_random_preset_cake()
    context.user_data["cake_id"] = cake.id
    show_cake(update, context)


def unshow_cake(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    del context.user_data["cake_id"]
    if context.user_data.get("back_step"):
        list_cakes(update, context)
    else:
        start(update, context)


def show_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if not context.user_data.get("cake_id"):
        context.user_data["cake_id"] = query.data.split("_")[-1]
    cake = get_cake(context.user_data["cake_id"])

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    image_url = f'{settings.SITE_URL}{cake.image.url}'
    caption = f"""Торт {cake.title}
        Количество уровней: {cake.level.title}
        Форма: {cake.form.title}
        Топинг: {cake.topping.title}
        Ягода: {cake.berry.title}
        Декор: {cake.decor.title}

        Цена: {cake.price} рублей
        """
    context.user_data["cake_for_order"] = cake
    keyboard = [
        [InlineKeyboardButton("Заказать", callback_data="get_data_for_cake")],
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="unshow_cake",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
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
        CallbackQueryHandler(recomend_cake, pattern="^recomend_cake$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(unshow_cake, pattern="^unshow_cake$")
    )
    return updater.dispatcher

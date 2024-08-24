from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

from .common_handler_functions import build_button_table
from .db_querrys import get_cake, get_presets_cakes, get_random_preset_cake


def list_cakes(update: Update, context: CallbackContext):
    # context.user_data["salon_id"] = None
    # context.user_data["specialist_id"] = None
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
    query.edit_message_text(
        text="Готовые торты:",
        reply_markup=InlineKeyboardMarkup(build_button_table(buttons, cols=2)),
    )


def recomend_cake(update: Update, context: CallbackContext):
    cake = get_random_preset_cake()
    context.user_data["cake_showed_back_step"] = "start"
    context.user_data["cake_showed_next_step"] = "v"
    context.user_data["cake_id"] = cake.id
    show_cake(update, context)


def unshow_cake(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    context.bot.send_message("")
    update.callback_query = context.user_data["cake_showed_back_step"]
    context.user_data["cake_showed_back_step"] = None


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
    context.user_data["cake_showed_back_step"] = "start"
    # Определяем кнопки
    keyboard = [
        [
            InlineKeyboardButton(
                "Назад",
                callback_data=context.user_data["cake_showed_back_step"],
            ),
        ],
        [InlineKeyboardButton("Выбрать", callback_data="unshow_cake")],
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
        CallbackQueryHandler(recomend_cake, pattern="^recomend_cake$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(unshow_cake, pattern="^unshow_cake$")
    )
    return updater.dispatcher

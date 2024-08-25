# Адрес доставки
# Дата доставки
# Время доставки (предупредить, что если до 24 часов - цена на 20% выше)
# Поделиться номером
# Пожелание для доставщика

# Вывод заказов для пользователя
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)
    
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common_handler_functions import build_button_table
from .db_querrys import (
    get_berries,
    get_berry,
    get_decor,
    get_decors,
    get_form,
    get_forms,
    get_level,
    get_levels,
    get_topping,
    get_toppings,
    check_and_add_phone_number
)


def get_data_for_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    button = [
        [InlineKeyboardButton("Пропустить", callback_data="skip_cake_caption")]
    ]
    try:
        query.edit_message_text(
            text="Хотите сделать надпись на торте? Укажите в сообщении",
            reply_markup=InlineKeyboardMarkup(button),
        )
    except(Exception):
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        context.bot.send_message(
            text="Хотите сделать надпись на торте? Укажите в сообщении",
            reply_markup=InlineKeyboardMarkup(button),
            chat_id=update.effective_chat.id
        )
    return "get_cake_caption"


def get_cake_caption(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["cake_caption"] = update.message.text if update.message else None
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Укажите адрес доставки:",
    )
    return "get_delivery_address"


def get_delivery_address(update: Update, context: CallbackContext):
    context.user_data["delivery_address"] = update.message.text
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Комментарий для курьера",
    )
    return "get_comment"


def get_comment(update: Update, context: CallbackContext):
    context.user_data["delivery_comment"] = update.message.text
    make_order(update, context)
    context.user_data['get_number_in_progress'] = True
    keyboard = [
        [
            KeyboardButton(
                "Поделиться номером", request_contact=True,
            )
        ]
    ]
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="""Укажите Ваш номер телефона с помощью нажатия на кнопку снизу,
    либо предоставьте контакт клиента""", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True))

def get_phone_number(update: Update, context: CallbackContext):
    if context.user_data.get('get_number_in_progress'):
        user = update.message.contact
        if update.message.contact:
            ReplyKeyboardRemove(True)
            context.user_data['get_number_in_progress'] = False
            # if user.user_id != context.user_data['client_id']:
                # create_client(user.user_id, user.first_name, user.last_name)
            context.user_data['client_id'] = user.user_id    
            check_and_add_phone_number(user.user_id, user.phone_number)
            # make_appointment(update, context)

def make_order(update: Update, context: CallbackContext):
    pass


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(MessageHandler(Filters.contact & ~Filters.command, get_phone_number))
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    get_data_for_cake, pattern="^get_data_for_cake$"
                )
            ],
            states={
                "get_cake_caption": [
                    CallbackQueryHandler(
                        get_cake_caption, pattern="^skip_cake_caption$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_cake_caption
                    ),
                ],
                "get_delivery_address": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_delivery_address
                    )
                ],
                "get_comment": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_comment
                    )
                ],
                "get_phone_number": [
                    MessageHandler(
                        Filters.contact & ~Filters.command, get_phone_number
                    )
                ]
            },
            fallbacks=[],
        )
    )

    return updater.dispatcher

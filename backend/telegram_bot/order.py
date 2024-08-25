# Адрес доставки
# Дата доставки
# Время доставки (предупредить, что если до 24 часов - цена на 20% выше)
# Поделиться номером
# Пожелание для доставщика

# Вывод заказов для пользователя
import datetime as dt


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
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
    check_and_add_phone_number,
    create_cake,
    get_berry,
    get_decor,
    get_form,
    get_level,
    get_topping,
    get_client,
    create_invoice,
    create_order
)
from .start import (
    WOKRDAY_END,
    WORKDAY_START,
)

ADMIN_ID = 283670670


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
    return "CAPTION"


def get_cake_caption(update: Update, context: CallbackContext):
    context.user_data["cake_caption"] = (
        update.message.text if update.message else ""
    )
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            "Укажите адрес доставки:",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Укажите адрес доставки:",
        )
    return "DELIVERY_ADDRESS"


def get_delivery_address(update: Update, context: CallbackContext):
    context.user_data["delivery_address"] = update.message.text
    show_comment_fetch(update, context)
    return "COMMENT"

def show_comment_fetch(update, context):
    query = update.callback_query
    button = [
        [InlineKeyboardButton("Пропустить", callback_data="skip_comment")]
    ]
    if query:
        query.answer()
        query.edit_message_text(
            text="Комментарий для курьера",
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Комментарий для курьера",
            reply_markup=InlineKeyboardMarkup(button),
        )


def get_comment(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        query.answer()
    context.user_data["delivery_comment"] = (
        update.message.text if update.message else ""
    )
    show_delivery_date(update, context)
    return "DELIVERY_DATE"


def show_delivery_date(update: Update, context: CallbackContext):
    query = update.callback_query
    today = dt.datetime.today()
    buttons = []
    if dt.datetime.now().hour < WOKRDAY_END:
        day_start = 1
    else:
        day_start = 2
    for day in range(day_start, day_start + 9):
        date = today + dt.timedelta(days=day)
        delivery_date = date.strftime("%m-%d")
        buttons.append(
            InlineKeyboardButton(
                delivery_date, callback_data=f"delivery_date_{delivery_date}"
            )
        )
    if query:
        query.answer()
        query.edit_message_text(
            text="Выберете дату доставки:",
            reply_markup=InlineKeyboardMarkup(
                build_button_table(buttons, cols=3)
            ),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Выберете дату доставки:",
            reply_markup=InlineKeyboardMarkup(
                build_button_table(buttons, cols=3)
            ),
        )


def get_delivery_date(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["delivery_date"] = query.data.split("_")[-1]
    show_delivery_time(update, context)
    return "DELIVERY_TIME"


def show_delivery_time(update: Update, context: CallbackContext):
    query = update.callback_query
    buttons = []
    for hour in range(WORKDAY_START, WOKRDAY_END + 1):
        buttons.append(
            InlineKeyboardButton(
                f"{hour:02}:00", callback_data=f"delivery_time_{hour}"
            )
        )
    query.edit_message_text(
        text="Выберете время доставки:",
        reply_markup=InlineKeyboardMarkup(
            build_button_table(buttons, cols=3)
        ),
    )


def get_delivery_time(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["delivery_time"] = query.data.split("_")[-1]
    show_phone_number(update, context)
    return 'PHONE_NUMBER'
    

def show_phone_number(update: Update, context: CallbackContext):
    keyboard = [
        [
            KeyboardButton(
                "Поделиться номером",
                request_contact=True,
            )
        ]
    ]
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="""Укажите Ваш номер телефона с помощью нажатия на кнопку снизу,
    либо предоставьте контакт клиента""",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )

def get_phone_number(update: Update, context: CallbackContext):
    user = update.message.contact
    if update.message.contact:
        ReplyKeyboardRemove(True)
        context.user_data["get_number_in_progress"] = False
        context.user_data["client_id"] = user.user_id
        check_and_add_phone_number(user.user_id, user.phone_number)
        make_order(update, context)

def make_order(update: Update, context: CallbackContext):
    if not context.user_data.get('preset_cake') and not context.user_data.get('recomend_cake'):
        
        level = get_level(context.user_data["cake_level_id"])
        form = get_form(context.user_data["cake_form_id"])
        topping = get_topping(context.user_data["cake_topping_id"])
        decor = get_decor(context.user_data.get("cake_decor_id") or None)
        berry = get_berry(context.user_data.get("cake_berry_id") or None)
        cake = create_cake(level, form, topping, berry, decor, caption=context.user_data.get("cake_caption") )
    elif(context.user_data.get('recomend_cake')):
        cake = context.user_data.get('recomend_cake')
    elif(context.user_data.get('preset_cake')):
        cake = context.user_data.get('preset_cake')
    client_id = context.user_data["client_id"]
    client = get_client(client_id)
    delivery_comment = context.user_data["delivery_comment"]
    delivery_time = context.user_data["delivery_time"]
    delivery_date = f'{dt.datetime.now().year}-{context.user_data["delivery_date"]}'
    delivery_address = context.user_data["delivery_address"]
    invoice = create_invoice(client, cake.price, delivery_date, delivery_time)
    order = create_order(client,cake,delivery_date, delivery_time, delivery_address, invoice, delivery_comment)
    context.bot.send_message(chat_id=ADMIN_ID, text=f"""
Заказ №{order.id}:
Торт: {cake.title or 'сборный'}
Уровни: {cake.level.title}
Форма: {cake.form.title}
Топпинг: {cake.topping.title}
Ягода: {cake.berry and cake.berry.title or '-'}
Декор: {cake.decor and cake.decor.title or '-'}
Надпись: {cake.caption or '-'}

Цена: {invoice.amount}

Доставка:
{delivery_date} в {delivery_time}
Адрес: {delivery_address}
Комментарий: {delivery_comment}

Номер телефона:
{client.phone_number}""")
    order_end(update, context)
    
def order_end(update: Update, context: CallbackContext):
    query = update.callback_query
    button = [
        [InlineKeyboardButton("В меню", callback_data="start")]
    ]
    if query:
        query.answer()
        query.edit_message_text(
            text="Заказ принят",
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Заказ принят",
            reply_markup=InlineKeyboardMarkup(button),
        )
    return ConversationHandler.END

def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    get_data_for_cake, pattern="^get_data_for_cake$"
                )
            ],
            states={
                "CAPTION": [
                    CallbackQueryHandler(
                        get_cake_caption, pattern="^skip_cake_caption$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_cake_caption
                    ),
                ],
                "COMMENT": [
                    CallbackQueryHandler(
                        get_comment, pattern="^skip_comment$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_comment
                    ),
                ],
                "PHONE_NUMBER": [
                    MessageHandler(Filters.contact & ~Filters.command, get_phone_number)
                ],
                "DELIVERY_ADDRESS": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_delivery_address
                    )
                ],
                "DELIVERY_DATE":[
                    CallbackQueryHandler(get_delivery_date, pattern="^delivery_date_")
                ],
                "DELIVERY_TIME":[
                    CallbackQueryHandler(get_delivery_time, pattern="^delivery_time_")
                ]
            },
            fallbacks=[],
        )
    )

    return updater.dispatcher

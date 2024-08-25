from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    Updater,
)

from .db_querrys import check_client, create_client, get_time_frame

time_frame = get_time_frame()

# Время начала рабочего дня
WORKDAY_START = time_frame.workday_start.hour

# Время окончания рабочего дня
WOKRDAY_END = time_frame.workday_end.hour

# Минимальное время доставки (в часах)
MINIMUM_LEDA_TIME = time_frame.minimum_lead_time

# Максимальное время ускоренной доставки (в часах)
MAXIMUM_EXPEDITED_LEAD_TIME = time_frame.maximum_expedited_lead_time

URL_AGREEMENT = "https://disk.yandex.ru/i/8a4x4M9KB8A3qw"


# Согласие на обработку ПД
def prestart_PD_request(update: Update, context: CallbackContext):
    context.user_data["user_initial"] = update.message.from_user
    keyboard = [[InlineKeyboardButton("Согласен", callback_data="reg_user")]]
    welcome_message = f"""
        Добро пожаловать в бота магазина тортов\\!
        Для продолжения работы с ботом нам потребуется Ваше согласие на обработку персональных данных\\.
        С документом Вы можете ознакомиться [по ссылке]({URL_AGREEMENT})\\.
        Нажимая "Согласен" \\- Вы даёте своё согласие и можете продолжать пользоваться ботом\\.
        """
    update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# Регистрация пользователя
def reg_user(update: Update, context: CallbackContext):
    user = context.user_data["user_initial"]
    if not check_client(user["id"]):
        create_client(
            user["id"],
            user["first_name"],
            user["last_name"],
            user["username"],
        )
    context.user_data["client_id"] = user["id"]
    start(update, context)


# Старт бота
# Если пользователя нет в бд - согласие ПД, регистрация
def start(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.user_data["client_id"] = update.effective_chat.id
    if not check_client(context.user_data["client_id"]):
        prestart_PD_request(update, context)
        return
    keyboard = [
        [InlineKeyboardButton("Готовые торты", callback_data="list_cakes")],
        [InlineKeyboardButton("Рекомендуем", callback_data="recomend_cake")],
        [InlineKeyboardButton("Собрать свой торт", callback_data="make_cake")],
        [InlineKeyboardButton("Заказы", callback_data="show_orders")],
    ]
    start_message = f"""Здравствуйте!
Заказы обрабатываются от {MINIMUM_LEDA_TIME} рабочих часов.
Рабочие часы: с {WORKDAY_START} до {WOKRDAY_END} мск"""
    query = update.callback_query
    try:
        if query:
            query.answer()
            query.edit_message_text(
                start_message, reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            update.message.reply_text(
                start_message, reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except(Exception):
        context.bot.send_message(
            text=start_message, reply_markup=InlineKeyboardMarkup(keyboard), chat_id=update.effective_chat.id
        )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(start, pattern="^start$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(reg_user, pattern="^reg_user$")
    )
    return updater.dispatcher
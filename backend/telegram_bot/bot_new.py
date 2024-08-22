import datetime as dt
import logging

from django.conf import settings
from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


from .db_querrys import check_client, create_client, get_time_frame
from .common_handler_functions import (
    get_phone_number
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Время начала рабочего дня
WORKDAY_START = None
# Время окончания рабочего дня
WOKRDAY_END = None
# Минимальное время доставки (в часах)
MINIMUM_LEDA_TIME = None
# Максимальное время ускоренной доставки (в часах)
MAXIMUM_EXPEDITED_LEAD_TIME = None

URL_AGREEMENT = "https://disk.yandex.ru/i/8a4x4M9KB8A3qw"


def reg_user(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
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


def reg_user_request(update: Update, context: CallbackContext):
    context.user_data["user_initial"] = update.message.from_user
    if not check_client(context.user_data["user_initial"]["id"]):
        keyboard = [
            [InlineKeyboardButton("Согласен", callback_data="register_user")]
        ]
        update.message.reply_text(
            f"""
    Добро пожаловать в бота магазина тортов\\!
    Для продолжения работы с ботом нам потребуется Ваше согласие на обработку персональных данных\\.
    С документом Вы можете ознакомиться [по ссылке]({URL_AGREEMENT})\\.
    Нажимая "Согласен" \\- Вы даёте своё согласие и можете продолжать пользоваться ботом\\.
    """,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        start()


def start(update: Update, context: CallbackContext):
    context.user_data["client_id"] = update.effective_chat.id
    if not check_client(context.user_data["client_id"]):
        reg_user_request(update, context)
        return
    keyboard = [
        [
            InlineKeyboardButton(
                "Наши предложения", callback_data="list_cakes"
            )
        ],
        [
            InlineKeyboardButton("Рекомендация торта", callback_data="recomend_cake")
        ],
        [
            InlineKeyboardButton(
                "Собрать свой торт", callback_data="make_cake"
            )
        ],
        [
            InlineKeyboardButton(
                "Заказы", callback_data="orders"
            )
        ],
    ]

    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            "Выберите услугу, салон или мастера",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        update.message.reply_text(
            # !!!!!!!!!!! берем время из бд first элемента
            f"""Здравствуйте!
            Заказы обрабатываются от {MINIMUM_LEDA_TIME} рабочих часов.
            Рабочие часы: с {WORKDAY_START} до {WOKRDAY_END} мск""",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main():
    time_frame = get_time_frame()
    # Время начала рабочего дня
    WORKDAY_START = time_frame.workday_start
    # Время окончания рабочего дня
    WOKRDAY_END = time_frame.workday_end
    # Минимальное время доставки (в часах)
    MINIMUM_LEDA_TIME = time_frame.minimum_lead_time
    # Максимальное время ускоренной доставки (в часах)
    MAXIMUM_EXPEDITED_LEAD_TIME = time_frame.maximum_expedited_lead_time

    updater = Updater(settings.BOT_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(start, pattern="^start$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(reg_user, pattern="^register_user$")
    )
    # updater.dispatcher.add_handler(
    #     CallbackQueryHandler(cake_handler, pattern="^cake_handle")
    # )
    # updater.dispatcher.add_handler(
    #     CallbackQueryHandler(date_handler, pattern="^date_handle")
    # )
    # updater.dispatcher.add_handler(
    #     CallbackQueryHandler(time_handler, pattern="^time_handle")
    # )
    updater.start_polling()
    updater.idle()

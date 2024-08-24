import datetime as dt

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import CallbackContext

from .db_querrys import (
    check_and_add_phone_number,
    create_client,
    create_order,
    get_client,
)


def build_button_table(buttons, cols):
    button_table = [
        buttons[i : i + cols] for i in range(0, len(buttons), cols)
    ]
    return button_table


def get_phone_number(update: Update, context: CallbackContext):
    if context.user_data.get("get_number_in_progress"):
        user = update.message.contact
        if update.message.contact:
            ReplyKeyboardRemove(True)
            context.user_data["get_number_in_progress"] = False
            if user.user_id != context.user_data["client_id"]:
                create_client(user.user_id, user.first_name, user.last_name)
                context.user_data["client_id"] = user.user_id
            check_and_add_phone_number(user.user_id, user.phone_number)
            make_appointment(update, context)
            # check_and_create_appointment(update, context)

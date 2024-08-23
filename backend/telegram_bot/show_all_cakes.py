from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater
)
from .db_querrys import (
    get_presets_cakes
)


def list_cakes(update: Update, context: CallbackContext):
    # context.user_data["salon_id"] = None
    # context.user_data["specialist_id"] = None
    query = update.callback_query
    query.answer()
    cakes = get_presets_cakes()

    # Тут красоту наводим
    keyboard = [
        [
            InlineKeyboardButton(
                f"{cake.title}",
                callback_data=f"salon_id_{cake.id}",
            )
        ] for cake in cakes
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="start")])
    query.edit_message_text(
        text="Выберите торт:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(list_cakes, pattern="^list_salons$")
    )
    return updater.dispatcher

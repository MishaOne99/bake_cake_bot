from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

from .common_handler_functions import build_button_table
from .db_querrys import get_berries, get_forms, get_levels, get_toppings


def choose_levels(update: Update, context: CallbackContext):
    query = update.callback_query
    levels = get_levels()

    buttons = [
        [
            InlineKeyboardButton(
                level.title,
                callback_data=f"cake_level_{level.id}",
            )
        ]
        for level in levels
    ]
    buttons.append([
        InlineKeyboardButton(
            "Назад",
            callback_data="start",
        )]
    )

    query.edit_message_text(
        text="Выберите количество уровней торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_form(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["cake_level_id"] = query.data.split("_")[-1]
    forms = get_forms()

    buttons = [
        [
            InlineKeyboardButton(
                form.title,
                callback_data=f"cake_form_{form.id}",
            )
        ]
        for form in forms
    ]
    buttons.append([
        InlineKeyboardButton(
            "Назад",
            callback_data="choose_levels",
        )]
    )

    query.edit_message_text(
        text="Выберите форму торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_topping(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["cake_form_id"] = query.data.split("_")[-1]
    toppings = get_toppings()

    buttons = [
        InlineKeyboardButton(
            topping.title,
            callback_data=f"cake_topping_{topping.id}",
        ) for topping in toppings
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append([
        InlineKeyboardButton(
            "Назад",
            callback_data="choose_form",
        )]
    )

    query.edit_message_text(
        text="Выберите топпинг для торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_berries(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["cake_topping_id"] = query.data.split("_")[-1]
    berries = get_berries()

    buttons = [
        InlineKeyboardButton(
            berry.title,
            callback_data=f"cake_berry_{berry.id}",
        ) for berry in berries
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append([
        InlineKeyboardButton(
            "Назад",
            callback_data="choose_form",
        )]
    )

    query.edit_message_text(
        text="Выберите топпинг для торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def handlers_custom_cake_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_levels, pattern="^make_cake$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_levels, pattern="^choose_levels$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_form, pattern="^cake_level_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_form, pattern="^choose_form$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_topping, pattern="^cake_form_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_topping, pattern="^choose_topping$")
    )
    return updater.dispatcher

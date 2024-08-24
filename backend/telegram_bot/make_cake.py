from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

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
)


def choose_levels(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
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
    buttons.append(
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="start",
            )
        ]
    )

    query.edit_message_text(
        text="Выберите количество уровней торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_form(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    level_id = query.data.split("_")[-1]
    if level_id.isnumeric():
        context.user_data["cake_level_id"] = level_id
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
    buttons.append(
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="choose_levels",
            )
        ]
    )

    query.edit_message_text(
        text="Выберите форму торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_topping(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    form_id = query.data.split("_")[-1]
    if form_id.isnumeric():
        context.user_data["cake_form_id"] = form_id
    toppings = get_toppings()

    buttons = [
        InlineKeyboardButton(
            topping.title,
            callback_data=f"cake_topping_{topping.id}",
        )
        for topping in toppings
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="choose_form",
            )
        ]
    )

    query.edit_message_text(
        text="Выберите топпинг для торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_berries(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    topping_id = query.data.split("_")[-1]
    if topping_id.isnumeric():
        context.user_data["cake_topping_id"] = topping_id
    berries = get_berries()

    buttons = [
        InlineKeyboardButton(
            berry.title,
            callback_data=f"cake_berry_{berry.id}",
        )
        for berry in berries
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(
        [
            InlineKeyboardButton(
                "Пропустить",
                callback_data="cake_berry_",
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="choose_topping",
            )
        ]
    )

    query.edit_message_text(
        text="Выберите ягоды для торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def choose_decor(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    berry_id = query.data.split("_")[-1]
    if berry_id.isnumeric() or not berry_id:
        context.user_data["cake_berry_id"] = berry_id
    decors = get_decors()

    buttons = [
        InlineKeyboardButton(
            decor.title,
            callback_data=f"cake_decor_{decor.id}",
        )
        for decor in decors
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(
        [
            InlineKeyboardButton(
                "Пропустить",
                callback_data="cake_decor_",
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="choose_berries",
            )
        ]
    )

    query.edit_message_text(
        text="Выберите декор для торта:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def show_assembled_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    decor_id = query.data.split("_")[-1]
    context.user_data["cake_decor_id"] = decor_id
    level_id = context.user_data["cake_level_id"]
    form_id = context.user_data["cake_form_id"]
    topping_id = context.user_data["cake_topping_id"]
    berry_id = context.user_data["cake_berry_id"]
    level = get_level(level_id)
    form = get_form(form_id)
    topping = get_topping(topping_id)
    berry = get_berry(berry_id) if berry_id else None
    decor = get_decor(decor_id) if decor_id else None
    price = (
        level.price
        + form.price
        + topping.price
        + (berry.price if berry else 0)
        + (decor.price if decor else 0)
    )
    not_selected = "Не выбрано"

    message = f"""Торт
        Количество уровней: {level.title}
        Форма: {form.title}
        Топинг: {topping.title}
        Ягода: {berry.title if berry else not_selected}
        Декор: {decor.title if decor else not_selected}

        Цена: {price} рублей
        """

    buttons = [
        [
            InlineKeyboardButton(
                "Заказать",
                callback_data="order",
            )
        ],
        [
            InlineKeyboardButton(
                "Назад",
                callback_data="choose_decors",
            )
        ],
        [
            InlineKeyboardButton(
                "Главное меню",
                callback_data="start",
            )
        ],
    ]

    query.edit_message_text(
        text=message,
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
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_berries, pattern="^cake_topping_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_berries, pattern="^choose_berries$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_decor, pattern="^cake_berry_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(choose_decor, pattern="^choose_decors$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(show_assembled_cake, pattern="^cake_decor_")
    )

    return updater.dispatcher

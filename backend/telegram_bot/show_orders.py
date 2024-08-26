from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater

from .db_querrys import get_orders_by_client


def show_orders(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    orders = get_orders_by_client(update.effective_chat.id)
    back_button = [[InlineKeyboardButton("Назад", callback_data='start')]]
    buttons_markup = InlineKeyboardMarkup(back_button)
    if not orders:
        query.edit_message_text(
            text="У вас отсутствуют активные заказы.",
            reply_markup=buttons_markup,
        )
    else:
        message = ""
        for order in orders:
            message = f"""{message}\n
Заказ №{order.id}:
    Торт: {order.cake.title or 'сборный'}
    Уровни: {order.cake.level.title}
    Форма: {order.cake.form.title}
    Топпинг: {order.cake.topping.title}
    Ягода: {order.cake.berry and order.cake.berry.title or '-'}
    Декор: {order.cake.decor and order.cake.decor.title or '-'}
    Надпись: {order.cake.caption or '-'}
Цена: {order.invoice.amount}
Доставка:
    {order.delivery_date} в {order.delivery_time}
    Адрес: {order.delivery_address}
    Комментарий: {order.comment}"""
        query.edit_message_text(
            text=message,
            reply_markup=buttons_markup,
        )        

def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(show_orders, pattern="^show_orders$")
    )
    return updater.dispatcher

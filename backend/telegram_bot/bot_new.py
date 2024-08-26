import logging

from django.conf import settings
from telegram.ext import Updater

from .make_cake import handlers_register as make_cake
from .order import handlers_register as make_order
from .show_cakes import handlers_register as show_cakes
from .show_orders import handlers_register as show_orders
from .start import handlers_register as start_reg

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    updater.dispatcher = start_reg(updater)
    updater.dispatcher = show_cakes(updater)
    updater.dispatcher = make_cake(updater)
    updater.dispatcher = make_order(updater)
    updater.dispatcher = show_orders(updater)
    updater.start_polling()
    updater.idle()

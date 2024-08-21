from django.core.management.base import BaseCommand
# from telegram_bot.bot_new import main


class Command(BaseCommand):
    help = 'Запуск бота для магазина тортиков'

    def handle(self, *args, **kwargs):
        self.stdout.write("Запуск бота...")
        # main()

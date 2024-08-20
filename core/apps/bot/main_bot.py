from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from environs import Env
import os


env = Env()
env.read_env()
token = env.str("TG_BOT_TOKEN")
bot = TeleBot(token)
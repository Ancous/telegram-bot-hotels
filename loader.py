from telebot import TeleBot

from config_data.config import SiteSetting

token = SiteSetting()
API_TOKEN = SiteSetting().BOT_TOKEN.get_secret_value()
bot = TeleBot(token=API_TOKEN)

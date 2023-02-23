import telebot
from setting import SiteSetting


token = SiteSetting()
API_TOKEN = token.TOKEN.get_secret_value()
bot = telebot.TeleBot(API_TOKEN)


from telebot.types import Message

from config_data.config import Time
from loader import bot


@bot.message_handler()
def handle_text(message: Message):
    if message.text == "Hello":
        bot.send_message(message.from_user.id, text=Time.times_day())
    else:
        bot.send_message(message.from_user.id, text="Sorry I do not understand you")

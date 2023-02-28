from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['hello_world'])
def send_welcome(message: Message):
    bot.reply_to(message, """Hello. I am not the world, I am a stupid bot executing programmed commands""")

from telegram_API.core import bot
from setting import Time


@bot.message_handler(commands=['hello-world'])
def send_welcome(message):
    return bot.reply_to(message, """Hello. I am not the world, I am a stupid bot executing programmed commands""")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Привет":
        return bot.send_message(message.from_user.id, text=Time.times_day())
    else:
        return bot.send_message(message.from_user.id, text="Sorry I do not understand you")


launch = bot.infinity_polling()


if __name__ in "__main__":
    send_welcome()
    handle_text()

    launch()

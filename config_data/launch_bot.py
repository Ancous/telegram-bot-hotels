import os
import telebot

from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN_BOT"))
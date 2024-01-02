"""
Модуль запуска бота
"""

from config_data.variables_constants_bot import VariablesConstantsBot
import handlers  # noqa

if __name__ in "__main__":

    while True:
        try:
            VariablesConstantsBot.BOT.polling(none_stop=True)
        except Exception as _ex:
            print(_ex)

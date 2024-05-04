import telebot
from config import currency, TOKEN
from extensions import APIException, ValuesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Для начала работы пожалуйста введите команду боту в формате:\n<название валюты>\
<в какую валюту нужно сделать перевод>\
<сумма для перевода>\n Список всех доступных валют по команде: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        currencies = message.text.split(' ')
        if len(currencies) != 3:
            raise APIException('Слишком много параметров. Повторите ввод.')
        quote, base, amount = currencies
        total_base = ValuesConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Сумма вашего перевода по схеме {quote} в {base} номиналом {amount} ед. на текущий момент составляет {total_base}.'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

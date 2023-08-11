import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter



bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = (f'Приветствую Вас {message.from_user.first_name} \n'\
           f'Для получения цены на валюту, отправьте сообщение в формате:\n'
           '<имя валюты цену которой вы хотите узнать>\n'
           '<имя валюты, в которой надо узнать цену первой валюты>\n'
           '<количество первой валюты>.\nНапример: USD RUB 1000\n'
           'Для получения списка доступных валют, введите команду /values.')
    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text ='Доступные валюты для перевода:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        data_values = message.text.split(' ')


        if len(data_values) > 3:
            raise ConvertionException('Вы ввели слишком много параметров')
        elif len(data_values) < 3:
            raise ConvertionException('Вы ввели слишком мало параметров')


        quote, base, amount = data_values
        total_base = Converter.get_price(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text =f'{amount} {quote} = {total_base} {base},\n'
        bot.send_message(message.chat.id, text, parse_mode='html')


bot.polling(none_stop=True)
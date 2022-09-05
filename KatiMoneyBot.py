import telebot
from config import TOKEN, currency
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

# Starting a conversation with KatiMoneyBot
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "For now, please enter following data :" \
           "\nCurrency \nTransfer to what kind of currency " \
           "\nAmount of transfering currency " \
           "\nTo see a list of currencies, please type: /values"
    bot.reply_to(message, text)


# Give a list of currencies to a user
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies: '
    for item in currency:
        text = '\n'.join((text, item,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        # Preventing from typing more parameters then needed
        if len(values) != 3:
            raise ConvertionException("Not enough or too much parameters.")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Mistake on your side. \n {e}')
    except Exception as e:
        bot.reply_to(message, f"Can not process your command, sorry. Try again. \n {e}")
    else:
        text = f"Price for {amount} {quote} in {base} = {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()

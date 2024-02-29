import telebot

from config import keys, TOKEN
from exception import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "issue"])
def issue(message: telebot.types.Message):
    text = "Welcome to the most popular Money Changer! " \
           "\n < 1. Please Enter a currency to find out its price > \n <2. Enter the name of the currency, " \
           "in which you want to know " \
           "the price of the first currency> \n <3. Enter the amount of the first currency>\n \
 Available currencies: /values"

    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Currencies:"
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def get_price(message: telebot.types.Message):

    try:
        parameters = list(map(lambda i: i.lower(), message.text.split(" ")))

        if len(parameters) != 3:
            raise APIException("Enter required parameters (it should be 3)")

        base, quote, amount = parameters

        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Incorrect value. Please try again later \n{e}")

    except Exception as e:
        bot.reply_to(message, f"Something wrong. Please try again \n{e}")
    else:
        text = f"Price of {amount} {base} in {quote}: {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

# import requests
# r = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR")
# print(r.content)

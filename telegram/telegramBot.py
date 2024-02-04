import telebot 
import requests 
import time
API_KEY="6523268004:AAHTrXHEmQVYRvnYXtJrBf7ZX2bChnF_o1A"
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=["hello"])
def hello(message):
    bot.reply_to(message, "Hello!, I am Smarti Bot and I will be here to help you in the manage of your Water Park")

@bot.message_handler(commands=["hello2"])
def hello2(message):
    bot.send_message(message.chat.id, "Hello!, I am Smarti Bot and I will be here to help you in the manage of your Water Park")


#TEMPERATURE
def temperature_request(message):
    request = message.text.split()
    if len(request)<2 or request[0].lower() not in "temperature":
        return False
    else:
        return True

@bot.message_handler(func=temperature_request)
def send_temperature(message):
    bot.send_message(message.chat.id, "The current temperature of the room is: 28 degrees")



#pH-sensor
def ph_request(message):
    request = message.text.split()
    if len(request)<2 or request[0].lower() not in "ph":
        return False
    else:
        return True

@bot.message_handler(func=ph_request)
def send_ph(message):
    bot.send_message(message.chat.id, "The current level of PH in the water is: 7")


#water level
def water_request(message):
    request = message.text.split()
    if len(request)<2 or request[0].lower() not in "water":
        return False
    else:
        return True

@bot.message_handler(func=water_request)
def send_water(message):
    bot.send_message(message.chat.id, "The current level of the water is: 1.2m")


#bot.polling()


#Automatic notification - could work in any part of the project
def telegram_bot_sendtext(bot_message):
   token = "6523268004:AAHTrXHEmQVYRvnYXtJrBf7ZX2bChnF_o1A"
   chat_id = "1227359148"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + bot_message 
   results = requests.get(url_req)
   print(results.json())


time.sleep(10)
telegram_bot_sendtext("Hello there!")

bot.polling()
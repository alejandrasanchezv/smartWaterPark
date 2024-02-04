import telebot 
import requests 
import time
import json

API_KEY="6523268004:AAHTrXHEmQVYRvnYXtJrBf7ZX2bChnF_o1A"
bot = telebot.TeleBot(API_KEY)

'''
class TelegramMqtt(object):
    def __init__(self) -> None:
        pass

    def onMsgReceived(device1, userdata, msg):
        print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")
        data = json.loads(msg.payload)
        topic = msg.topic

        userID = topic.split("/")[3]
        print(f'userID: {userID}')
        rideID = topic.split("/")[5]
        print(f'rideID: {rideID}')
        dataType = topic.split("/")[6]
        print(f'dataType: {dataType}')
        

        for user in db["users"]:
            if user["userID"] == int(userID):
                for ride in user["rides"]:
                    if ride["rideID"] == int(rideID):
                        sendThingSpeak(userID, rideID, dataType, data)


'''



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

if __name__ == "__main__":
    time.sleep(10)
    telegram_bot_sendtext("Hello there!")

    bot.polling()
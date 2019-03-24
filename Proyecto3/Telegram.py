import telebot

class Telegram:

    def __init__(self,keybot):
        self.bot = telebot.TeleBot(str(keybot))
    
    def sendMessage(self,message,idChat):
        self.bot.send_message(str(idChat), str(message))
    
    def sendImage(self,image,idChat):
        photo = open(str(image), 'rb')
        self.bot.send_photo(str(idChat), photo)
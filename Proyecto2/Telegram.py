import requests

class Telegram:

    def __init__(self,keybot):
        self.url = "https://api.telegram.org/bot"+ str(keybot) +"/sendMessage"
    
    def sendMessage(self,message,idChat):
        session = requests.Session()
        response = session.post(self.url, data={'chat_id':str(idChat) ,'disable_web_page_preview': '1', 'text': str(message),'parse_mode':'markdown'})
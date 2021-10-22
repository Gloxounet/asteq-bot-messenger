import random
from key import *
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

plats=["Crêpes","Sushis","Gauffres"]

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text') or message['message'].get('attachments'):
                
                    #response_sent_text = generate_message()
                    #send_message(recipient_id, response_sent_text)
                    if message['message'].get('text') and message['message']['text'] in plats:
                        response_sent_text = generate_message(message['message']['text'])
                        send_message(recipient_id, response_sent_text)
                    else:
                        buttons = convert_label_list_into_buttons(plats)
                        send_message_button(recipient_id, "Hey ! Voici ce que le BDA te propose aujourd'hui. Qu'est-ce qui te fait envie :",buttons)


    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def generate_message(response):
    # return selected item to the user
    return "C'est noté ! Tu peux venir retirer tes" + response + "dans 10min au P124 ! Bon appétit ;)"

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def send_message_button(recipient_id, text, buttons) :
    bot.send_button_message(recipient_id, text, buttons)
    return "sucess"

def convert_label_list_into_buttons(liste) :
    buttons = []
    for label in liste :
        button = {
            "type":"postback",
            "title":f"{label}",
            "payload": "DEVELOPER_DEFINED_PAYLOAD"
          }
        buttons.append(button)
    return buttons
        

if __name__ == "__main__":
    app.debug = True
    app.run()
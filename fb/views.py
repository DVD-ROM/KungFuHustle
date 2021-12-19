from django.shortcuts import render
from django.views import generic
from django.http.response import Http404, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint 
import json 
import requests
from dotenv import load_dotenv
import os

# Create your views here.

class fbView(generic.View):
    def get(self, request, *args, **kwargs):
        VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
        mode = self.request.GET['hub.mode']
        token = self.request.GET['hub.verify_token']
        challenge = self.request.GET['hub.challenge']

        if (mode and mode == "subscribe" and token and token == VERIFY_TOKEN):
            pprint('WEBHOOK VERIFIED')
            return HttpResponse(challenge)
        else:
            return HttpResponse(status=403)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        payloadAsDictionary = json.loads(self.request.body.decode('utf-8'))
       
        if (payloadAsDictionary['object'] == 'page'):
            for entry in payloadAsDictionary['entry']:
                for webhookEvent in entry['messaging']:
                    if 'message' in webhookEvent:
                        handleMessage(webhookEvent['sender']['id'], webhookEvent['message'])  
                    elif 'postback' in webhookEvent:
                        handlePostback(webhookEvent['sender']['id'], webhookEvent['postback'])
                    
            return HttpResponse()
        else: 
            return HttpResponse(status=404)



def handleMessage(sender_psid, received_message):
    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
    # are sent as attachments and must be handled accordingly. 
    if 'text' in received_message:
        response = {
            "text": f'You sent the message: "{received_message.text}". Now send me an image!'
        }
    elif 'attachments' in received_message:
        attachment_url = received_message['attachments'][0]['payload']['url']
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                            "title": "Is this the right picture?",
                            "subtitle": "Tap a button to answer.",
                            "image_url": attachment_url,
                            "buttons": [
                            {
                                "type": "postback",
                                "title": "Yes!",
                                "payload": "yes",
                            },
                            {
                                "type": "postback",
                                "title": "No!",
                                "payload": "no",
                            }
                        ],
                    }]
                }
            }
        }
        

    callSendAPI(sender_psid, response)  


def handlePostback(sender_psid, received_postback):
    payload = received_postback.payload
    if (payload == 'yes'):
        response = {"text": "Thanks!"}
    elif (payload == 'no'):
        response = {"text": "Oops, try sending another image."}

    callSendAPI(sender_psid, response)

def callSendAPI(sender_psid, response):
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')        
    post_message_url = f'https://graph.facebook.com/v12.0/me/messages?access_token={FACEBOOK_ACCESS_TOKEN}' 
    
    response_msg = json.dumps(
        { "recipient": {"id":sender_psid}, 
          "message":   {"text":response}
    })
    
    status = requests.post(
        post_message_url, 
        headers={"Content-Type": "application/json"},
        data=response_msg
    )
    
    pprint(status.json())
   
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import json 
import requests
from dotenv import load_dotenv
import os
import logging
from fb.services.config import Config
from functools import wraps 
from fb.services.security import validate_fb_request
from fb.services.receive import Receive
import fb.task_queue as task_queue
from django.views import generic

class WebhookView(TemplateView):
  
      # https://stackoverflow.com/questions/51710145/what-is-csrf-exempt/51710371
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs) 

    def get(self, request, *args, **kwargs):
        print("incoming!")
        VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
        mode = self.request.GET.get("hub.mode", '')
        token = self.request.GET.get("hub.verify_token", '')
        challenge = self.request.GET.get("hub.challenge", '')
        
        if (mode == "subscribe" and token == VERIFY_TOKEN):
            print('WEBHOOK VERIFIED')
            print(challenge)
            print(isinstance(challenge, str))
            response = HttpResponse(challenge)
            response.status_code = 200
            return response
        else:
            print("The mode is " + mode)
            print("The token is " + token)
            print("gonna return 403")
            return HttpResponse(status=403)
  
    @validate_fb_request
    def post(self, request, *args, **kwargs):
        bodyAsDict = json.loads(self.request.body.decode('utf-8'))
       
        print("Received webhook")
        print(bodyAsDict)

        # Check if this is an event from a page subscription, eg. KF Club 
        if (bodyAsDict['object'] == 'page'):
            task_queue.schedulePostToWebhook(bodyAsDict)
            return HttpResponse("EVENT_RECEIVED",status=200)
        else: 
            return HttpResponse(status=404)


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
    
    print(status.json())


def handlePostToWebhook(bodyAsDict):
    # Iterate over every entry - Facebook may batch several entries into one request
    for entry in bodyAsDict['entry']:
        for webhookEvent in entry['messaging']:

            # Discard uninteresting events
            if ("read" in webhookEvent):
                print("Got a read event")
                return
            elif ("delivery" in webhookEvent): 
                print("Got a delivery event")
                return
            elif (webhookEvent["message"] and webhookEvent["message"]["is_echo"]): 
                print("Got an echo of our send, mid = " + webhookEvent.message.mid)
                return

            receiveMessage = Receive(webhookEvent) 
            return receiveMessage.handleMessage()
    
   
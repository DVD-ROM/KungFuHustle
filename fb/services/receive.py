from fb.services.response import Response
from fb.services.graph_api import GraphApi
import threading

class Receive:
    def __init__(self, webHookEvent):
        self.webhookEvent = webHookEvent

    def handleMessage(self):
        event = self.webhookEvent
        
        try: 
            if (event.message):
                message = event.message
                if (message.postback):
                    responses = self.handlePostback()
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            responses = {"text": "An unexpected error occurred"}

        if isinstance(responses, list):
            delay = 0
            for response in responses: 
                self.sendMessage(response, delay*2)
                delay += 1
        else: 
            self.sendMessage(responses)
            
    def handlePostback(self): 
        postback = self.webhookEvent.postback

        if postback["payload"]:
            payload = postback["payload"] 
        elif postback["referral"] and postback["referral"]["type"] == "OPEN_THREAD":
            payload = postback["referral"]["ref"]

        return self.handlePayload(payload.upper())

    def handlePayload(self, payload):
        print(f'Received Payload: {payload} for {self.webhookEvent["sender"]["id"]}')

        responses = Response.makeMessage(payload.lower())
        
        return responses

    def sendMessage(self, response, delay=0):
        if ("delay" in response):
            delay = response["delay"]
            response.pop("delay")
        
        requestBody = {
            "recipient": {
                "id": self.webhookEvent["sender"]["id"],
            }, 
            "message": response
        }

        threading.Timer(delay, GraphApi.callSendApi(requestBody)).start()


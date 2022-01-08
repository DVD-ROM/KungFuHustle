from response import Response

class Receive:
    def __init__(self, webHookEvent):
        self.user = webHookEvent['sender']
        self.webhookEvent = webHookEvent

    def handleMessage(self):
        event = self.webhookEvent
        
        try: 
            if (event.message):
                message = event.message
                if (message.text):
                    responses = self.handleTextMessage()
                elif (message.postback):
                    responses = self.handlePostback()
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            responses = {"text": "An unexpected error occurred"}


    def handleTextMessage(self): 
        event = self.webhookEvent
    
        print(f'Received text: {event["message"]["text"]} for {self.user["id"]}')
        
        greeting = self.firstTrait(event['message']['nlp'], "wit$greetings")

        message = event.message.text.rstrip().lower()
        
        if (greeting and greeting.confidence > 0.8):
            response = Response.makeNuxMessage(self.user)


    def handlePostback(): 
        print("hi")

    def firstTrait():
        print("hi")
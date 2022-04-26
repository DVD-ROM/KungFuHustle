import json
import os

class MsgRetriever:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses.json')) as file:
        jsonReplies = json.load(file) 

    @classmethod
    def getMessageOfKey(cls, messageKey):
        keyTokens =  messageKey.split(".")
        jsonValue = cls.jsonReplies
    
        try:
            for token in keyTokens:
                jsonValue = jsonValue[token]
            return jsonValue
        except KeyError:
            return "No message found"






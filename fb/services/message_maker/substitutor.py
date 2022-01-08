import json
import os

class Substitutor:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses.json')) as file:
        jsonReplies = json.load(file) 

    @staticmethod
    def subIntoMsg(messageKey, values):
        message = Substitutor.getMessageOfKey(messageKey)
        if values is not None:
            for valueID, value in values.items():
                message.format(valueID, value)
        return message

    @classmethod
    def getMessageOfKey(cls, messageKey):
        keyTokens =  messageKey.split(".")
        jsonValue = cls.jsonReplies
        for token in keyTokens:
            jsonValue = jsonValue[token]
        return jsonValue





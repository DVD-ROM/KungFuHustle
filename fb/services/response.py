from fb.services.message_maker.msgRetriever import MsgRetriever
from fb.services.json_templates.template_maker import makeQuickReplyItem

class Response: 
    @classmethod
    def makeMessage(cls, messagesKey):
        preparedStatements = MsgRetriever.getMessageOfKey(messagesKey)
        if preparedStatements is None:
            return []
        else: 
            return cls.retrieveAllResponses(preparedStatements)

    @classmethod
    def retrieveAllResponses(cls, preparedStatements):
        responses = []
        for key, preparedStatement in preparedStatements.items():
            if isinstance(preparedStatement, dict):
                innerResponses = cls.retrieveAllResponses(preparedStatement)
                responses.append(innerResponses)
            else: 
                if key == "templates":
                    msg = cls.makeGenericTemplate(preparedStatement)
                else: 
                    msg = cls.makeText(preparedStatement)
                
                responses.push(msg)
            
        return responses


    @staticmethod
    def makeGenericTemplate(elements):
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        } 

    @staticmethod
    def makeText(text):
        return {
            "text": text 
        }

    
from message_maker.substitutor import Substitutor
from json_templates.template_maker import makeQuickReplyItem

class Response: 
    @staticmethod
    def makeQuickReply(text, quickReplies):
        response = {
            "text": text,
            "quick_replies": []
        }

        for quickReply in quickReplies:
            response["quick_replies"].append({
                "content_type": "text",
                "title": quickReply["title"],
                "payload": quickReply["payload"]
            })

        return response

    @staticmethod
    def makeNuxMessage(user):
        templateResponse = Substitutor.subIntoMsg("get_started.welcome", {
            "userFirstName": user.firstName 
        })
        welcome = Response.makeText(templateResponse)

        templateResponse = Substitutor.subIntoMsg("get_started.guidance", {})
        guide = Response.makeText(templateResponse)

        templateResponse = Substitutor.subIntoMsg("get_started.help", {})
        options = Response.makeQuickReply(templateResponse, [
            makeQuickReplyItem(
                title=Substitutor.subIntoMsg("menu.events"), 
                payload="EVENTS"
            ),
            makeQuickReplyItem(
                title=Substitutor.subIntoMsg("menu.class"),  
                payload="CLASS"
            ),
            makeQuickReplyItem(
                title=Substitutor.subIntoMsg("menu.exec"),
                payload="EXEC"
            ),
            makeQuickReplyItem(
                title = Substitutor.subIntoMsg("menu.restart"),
                payload = "RESTART"
            )
        ]) 

        return [welcome, guide, options]

   
    
    @staticmethod
    def makeText(text):
        return {
            "text": text 
        }

    
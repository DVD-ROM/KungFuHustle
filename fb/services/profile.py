from fb.services.graph_api import GraphApi
from fb.services.config import Config
from fb.services.message_maker.msgRetriever import MsgRetriever

class Profile:
    def __init__(self):
        return

    @staticmethod
    def setWebhook():
        GraphApi.callSubscriptionsAPI()
        GraphApi.callSubscribedApps()

    @staticmethod
    def setPageFeedWebhook():
        GraphApi.callSubscriptionsAPI("feed")
        GraphApi.callSubscribedApps("feed")

    @staticmethod
    def setThread():
        profilePayload = {
            **Profile.getGetStarted(),
            **Profile.getGreeting(),
            **Profile.getPersistentMenu()
        }
        print("here is profile payload")
        print(profilePayload)
        GraphApi.callMessengerProfileAPI(profilePayload)

    def setGetStarted(self):
        getStartedPayload = self.getGetStarted()
        GraphApi.callMessengerProfileAPI(getStartedPayload)

    def setGreeting(self):
        greetingPayload = self.getGreeting()
        GraphApi.callMessengerProfileAPI(greetingPayload)
    
    def setPersistentMenu(self):
        menuPayload = self.getPersistentMenu()
        GraphApi.callMessengerProfileAPI(menuPayload)

    def setWhiteListedDomains(self):
        domainPayload = self.getWhiteListedDomains()
        GraphApi.callMessengerProfileAPI(domainPayload)

    def getGetStarted():
        print("get started")
        return {
            "get_started": {
                "payload": "GET_STARTED"
            }
        }

    def getGreeting():
        print("get greeting")
        greetings = [Profile.getGreetingText()]
        return {
            "greeting": greetings
        }


    def getPersistentMenu():
        print("get persistent menu")
        menuItems = [Profile.getMenuItems()]
        return {
            "persistent_menu": menuItems
        }

    def getGreetingText():
        greeting = {
            "locale": "default",
            "text": MsgRetriever.getMessageOfKey("profile.greeting")
        }
        print(greeting)
        return greeting

    def getMenuItems():
        menu = {
            "locale": "default",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "title": MsgRetriever.getMessageOfKey("menu.about"),
                    "type": "postback",
                    "payload": "ABOUT_CLUB"
                },
                {
                    "title": MsgRetriever.getMessageOfKey("menu.contact"),
                    "type": "postback",
                    "payload": "CONTACT_INFO"
                },
                {
                    "title": MsgRetriever.getMessageOfKey("menu.class_info"),
                    "type": "postback",
                    "payload": "CLASS_INFO"
                },
                {
                    "title": MsgRetriever.getMessageOfKey("menu.class_schedule"),
                    "type": "postback",
                    "payload": "CLASS_SCHEDULE"
                },
                {
                    "title": MsgRetriever.getMessageOfKey("menu.demo"),
                    "type": "postback",
                    "payload": "DEMO_INQUIRY"
                }
            ]
        }
        print(menu)
        return menu

    @staticmethod
    def getWhiteListedDomains():
        whitelistedDomains = {
            "whitelisted_domains": Config.whitelistedDomains()
        }
        print(whitelistedDomains)
        return whitelistedDomains
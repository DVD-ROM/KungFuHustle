from graph_api import GraphApi
from config import Config
from message_maker.substitutor import Substitutor

class Profile:
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
        GraphApi.callMessengerProfileAPI(profilePayload)

    @staticmethod
    def setGetStarted():
        getStartedPayload = Profile.getGetStarted()
        GraphApi.callMessengerProfileAPI(getStartedPayload)
    


    @staticmethod
    def setGreeting():
        greetingPayload = Profile.getGreeting()
        GraphApi.callMessengerProfileAPI(greetingPayload)
    
    @staticmethod
    def setPersistentMenu():
        menuPayload = Profile.getPersistentMenu()
        GraphApi.callMessengerProfileAPI(menuPayload)


    @staticmethod
    def setWhiteListedDomains():
        domainPayload = Profile.getWhiteListedDomains()
        GraphApi.callMessengerProfileAPI(domainPayload)

    @staticmethod
    def getGetStarted():
        return {
            "get_started": {
                "payload": "GET_STARTED"
            }
        }

    @staticmethod
    def getGreeting():
        greetings = [Profile.getGreetingText()]
        return {
            "greeting": greetings
        }

    @staticmethod
    def getPersistentMenu():
        menuItems = [Profile.getMenuItems()]
        return {
            "persistent_menu": menuItems
        }


    @staticmethod
    def getGreetingText():
        greeting = {
            "text": Substitutor.getMessageOfKey("profile.greeting")
        }
        print(greeting)
        return greeting

    @staticmethod
    def getMenuItems():
        menu = {
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "title": Substitutor.getMessageOfKey("menu.events"),
                    "type": "postback",
                    "payload": "TRACK_ORDER"
                },
                {
                    "title": Substitutor.getMessageOfKey("menu.help"),
                    "type": "postback",
                    "payload": "CARE_HELP"
                },
                {
                    "title": Substitutor.getMessageOfKey("menu.suggestion"),
                    "type": "postback",
                    "payload": "CURATION"
                },
                {
                    "type": "web_url",
                    "title": Substitutor.getMessageOfKey("menu.shop"),
                    "url": Config.shopUrl,
                    "webview_height_ratio": "full"
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
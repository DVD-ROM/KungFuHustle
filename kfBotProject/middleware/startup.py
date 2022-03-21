from django.apps import AppConfig
from django.db.models.signals import pre_save
from fb.services.config import Config

class Startup(AppConfig):

    def ready(self):
        # importing model classes
        print(f'The app is listening on port {Config.port}')
        if (not Config.personas) and Config.appUrl and Config.verifyToken:
            print("Is this the first time running?\n" +
                  "Make sure to set the both the Messenger profile, persona " +
                  "and webhook by visiting:\n" +
                  Config.appUrl +
                  "/profile?mode=all&verify_token=" +
                  Config.verifyToken)
        
        if Config.pageId:
            print("Test your app by messaging:")
            print("https://m.me/${Config.pageId}")

        
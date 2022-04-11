from fb.services.config import Config
import requests

class GraphApi:
    @staticmethod
    def callSendApi(requestBody):
        url = f'{Config.apiUrl()}/me/messages'
        queryParams ={
             "access_token": Config.fbAccessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
     
        resp = requests.post(url, params=queryParams, json=requestBody, headers=headers)
        if not resp.status_code == requests.codes.ok:
            print(f"Couldn't send message: code {resp.status_code}") 

    @staticmethod
    def callMessengerProfileAPI(requestBody):
        print(f'Setting Messenger Profile for app {Config.appId}')
        url = f'{Config.apiUrl()}/me/messenger_profile'
        queryParams={
            "access_token": Config.fbAccessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
       
        resp = requests.post(url, params=queryParams, json=requestBody, headers=headers)
        if resp.status_code == requests.codes.OK:
            print('Request sent')
        else:
            print(f"Unable to callMessengerProfileAPI: code {resp.status_code}") 

    @staticmethod
    def callSubscriptionsAPI(customFields=None):
        print(f'Setting app {Config.appId} callback url to {Config.webhookUrl()}')

        fields = "messages, messaging_postbacks, messaging_optins, " + "message_deliveries, messaging_referrals"

        if not customFields is None:
            fields = fields + ", " + customFields

        print(fields)

        url = f'{Config.apiUrl()}/{Config.appId}/subscriptions'
        queryParams = {
            "access_token": f'{Config.appId}|{Config.fbAppSecret}',
            "object": "page",
            "callback_url": Config.webhookUrl(),
            "verify_token": Config.verifyToken,
            "fields": fields,
            "include_values": "true"
        }
        headers = {
            "Content-Type": "application/json"
        }
        print("Here is url")
        print(url)
        print(queryParams)
        print(headers)

        resp = requests.post(url, params=queryParams, headers=headers)
        if resp.status_code == requests.codes.OK:
            print('Request sent')
        else:
            print(f"Unable to callSubscriptionsAPI: code {resp.status_code}") 

    @staticmethod
    def callSubscribedApps(customFields=None):
        print(f'Subscribing app {Config.appId} to page {Config.pageId}')

        fields = "messages, messaging_postbacks, messaging_optins, " + "message_deliveries, messaging_referrals"

        if not customFields is None:
            fields = fields + ", " + customFields

        print(fields)

        url = f'{Config.apiUrl()}/{Config.pageId}/subscribed_apps'
        queryParams = {
            "access_token": Config.fbAccessToken,
            "subscribed_fields": fields
        }
        
        resp = requests.post(url, params=queryParams)
        if resp.status_code == requests.codes.OK:
            print('Request sent')
        else:
            print(f"Unable to callSubscribedApps: code {resp.status_code}")

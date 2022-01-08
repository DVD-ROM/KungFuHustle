from config import Config
import httpx
import json

class GraphApi:
    @staticmethod
    async def callSendApi(requestBody):
        url = f'{Config.apiUrl}/me/messages'
        queryParams ={
             "access_token": Config.fbAccessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams, json=requestBody, headers=headers)
            if not resp.status_code == httpx.codes.OK:
               print(f"Couldn't send message: code {resp.status_code}") 

    @staticmethod
    async def callMessengerProfileAPI(requestBody):
        print(f'Setting Messenger Profile for app {Config.appId}')
        url = f'{Config.apiUrl}/me/messenger_profile'
        queryParams={
            "access_token": Config.fbAccessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams, json=requestBody, headers=headers)
            if resp.status_code == httpx.codes.OK:
                print('Request sent')
            else:
                print(f"Unable to callMessengerProfileAPI: code {resp.status_code}") 

    @staticmethod
    async def callSubscriptionsAPI(customFields):
        print(f'Setting app {Config.appId} callback url to {Config.webhookUrl()}')

        fields = "messages, messaging_postbacks, messaging_optins, " + "message_deliveries, messaging_referrals"

        if not customFields is None:
            fields = fields + ", " + customFields

        print(fields)

        url = f'{Config.apiUrl}/{Config.appId}/subscriptions'
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

        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams, headers=headers)
            if resp.status_code == httpx.codes.OK:
                print('Request sent')
            else:
                print(f"Unable to callSubscriptionsAPI: code {resp.status_code}") 

    @staticmethod
    async def callSubscribedApps(customFields):
        print(f'Subscribing app {Config.appId} to page {Config.pageId}')

        fields = "messages, messaging_postbacks, messaging_optins, " + "message_deliveries, messaging_referrals"

        if not customFields is None:
            fields = fields + ", " + customFields

        print(fields)

        url = f'{Config.apiUrl}/{Config.pageId}/subscribed_apps'
        queryParams = {
            "access_token": Config.fbAccessToken,
            "subscribed_fields": fields
        }

        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams)
            if resp.status_code == httpx.codes.OK:
                print('Request sent')
            else:
                print(f"Unable to callSubscribedApps: code {resp.status_code}")

    @staticmethod
    async def getUserProfile(senderIgsid):
        url = f'{Config.apiUrl}/{senderIgsid}'
        queryParams = {
            "access_token": Config.fbAccessToken,
            "fields": "first_name, last_name, gender, locale, timezone"
        }
        async with httpx.AsyncClient() as client: 
            resp = await client.get(url, params=queryParams)
            if resp.status_code == httpx.codes.OK:
                userProfile = json.loads(resp.json())
                return {
                    "firstName": userProfile['first_name'],
                    "lastName": userProfile['last_name'],
                    "gender": userProfile['gender'],
                    "locale": userProfile['locale'],
                    "timezone": userProfile['timezone']
                }
            else:
                print(f"Could not load profile for {senderIgsid}: code {resp.status_code}")
                return None

    @staticmethod
    async def getPersonaAPI():
        print(f'Fetching personas for app {Config.appId}')

        url = f'{Config.apiUrl}/me/personas'

        queryParams = {
            "access_token": Config.fbAccessToken,
        }

        async with httpx.AsyncClient() as client: 
            resp = await client.get(url, params=queryParams)
            if resp.status_code == httpx.codes.OK:
                body = json.loads(resp.json())
                return body["data"]
            else:
                print(f"Unable to fetch personas for {Config.appId}: code {resp.status_code}")
                return None

    @staticmethod
    async def postPersonaAPI(name, profile_picture_url):
        requestBody = {
            "name": name, 
            "profile_picture_url": profile_picture_url
        }
        print(f'Creating a Persona for app {Config.appId}')
        print(requestBody)
        url = f'{Config.apiUrl}/me/personas'
        queryParams = {
            "access_token": Config.fbAccessToken,
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams, headers=headers, json=requestBody)
            if resp.status_code == httpx.codes.OK:
                print('Request sent')
                body = json.loads(resp.json())
                return body["id"]
            else:
                print(f"Unable to postPersonaAPI: code {resp.status_code}")
                return None

    @staticmethod
    async def callNLPConfigsAPI():
        print(f'Enable Built-in NLP for Page {Config.pageId}')
        url = f'{Config.apiUrl}/me/nlp_configs'
        queryParams = {
            "access_token": Config.fbAccessToken,
            "nlp_enabled": True
        }
        async with httpx.AsyncClient() as client: 
            resp = await client.post(url, params=queryParams)
            if resp.status_code == httpx.codes.OK:
                print('Request sent')
            else:
                print(f"Unable to activate built-in NLP: code {resp.status_code}")
    


import os


ENV_VARS = [
    "PAGE_ID",
    "APP_ID",
    "FACEBOOK_ACCESS_TOKEN",
    "FACEBOOK_APP_SECRET",
    "VERIFY_TOKEN",
    "APP_URL",
    "DJANGO_SETTINGS_MODULE",
    "LOCAL_ADDRESS",
    "SECRET_KEY",
    "SECRET_ADMIN_URL"
]

class Config:
    apiDomain = "https://graph.facebook.com"
    apiVersion = "v11.0"
    pageId = os.getenv('PAGE_ID')
    appId = os.getenv('APP_ID')
    fbAccessToken = os.getenv('FACEBOOK_ACCESS_TOKEN')
    fbAppSecret = os.getenv('FACEBOOK_APP_SECRET')
    verifyToken = os.getenv('VERIFY_TOKEN')
    appUrl = os.getenv('APP_URL')
    shopUrl = "hi"
    port = os.getenv('PORT') or 3000


    def apiUrl():
        return f'{Config.apiDomain}/{Config.apiVersion}'
    
    def webhookUrl():
        return f'{Config.apiUrl()}/webhook'


    # def pushPersona(persona):
    #     Config.personas[persona["name"]]

    def whitelistedDomains():
        return [Config.appUrl, Config.shopUrl]

    def checkEnvVariables():
        for varName in ENV_VARS:
            if os.getenv(varName) is None:
                print(f"WARNING: Missing the environment variable {varName}")
            elif varName == "APP_URL":
                url = os.getenv(varName)
                if not url.startswith("https://"):
                    print(f'Warning: Your {varName} does not begin with https://')

import hmac
from functools import wraps
from django.http.response import HttpResponseBadRequest
from fb.services.config import Config

def validate_fb_request(view):
    @wraps(view)
    def viewWithValidation(self, request, *args, **kwargs):
        print("here is request")
        print(request)
        if isFbRequestValid(request):
            return view(self, request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    return viewWithValidation


def isFbRequestValid(request):
    # https://stackoverflow.com/questions/6130768/return-none-if-dictionary-key-is-not-available
    # https://docs.djangoproject.com/en/4.0/ref/request-response/
    # https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-django-project-by-validating-incoming-twilio-requests

    signature = request.META["HTTP_X_HUB_SIGNATURE"]

    # https://stackoverflow.com/questions/39767297
    if signature is None:
        print("Couldn't find x-hub-signature in headers")
        return False
    else:
        elements = signature.split("=")
        signatureHash = elements[1]
        byte_key = bytes(Config.fbAppSecret,'UTF-8')
        print("here is request body")
        print(request.body)
        # https://stackoverflow.com/questions/22368190/django-cant-access-raw-post-data
        expectedHash = hmac.new(byte_key, request.body, digestmod='sha1').hexdigest()
        
        return hmac.compare_digest(expectedHash, signatureHash)
import hmac
from functools import wraps
from django.http.response import HttpResponseBadRequest
from fb.services.config import Config

def validate_fb_request(view):
    @wraps(view)
    def viewWithValidation(self, request, *args, **kwargs):
        if isFbRequestValid(request):
            return view(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    return viewWithValidation


def isFbRequestValid(request):
    # https://stackoverflow.com/questions/6130768/return-none-if-dictionary-key-is-not-available
    # https://docs.djangoproject.com/en/4.0/ref/request-response/
    # https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-django-project-by-validating-incoming-twilio-requests
    print('hello')
    print(request.META)
    signature = request.META["X-Hub-Signature"]

    if signature is None:
        print("Couldn't find x-hubt-signature in headers")
        return False
    else:
        elements = signature.split("=")
        signatureHash = elements[1]

        # https://stackoverflow.com/questions/22368190/django-cant-access-raw-post-data
        expectedHash = hmac.new(Config.fbAppSecret, request.body, digestmod='sha1').hexdigest()
        
        return hmac.compare_digest(expectedHash, signatureHash)
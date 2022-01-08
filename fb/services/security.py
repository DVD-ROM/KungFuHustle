import hmac
import os

class Security(object):
    def process_request(self, request):
        signature = request.get("x-hub-signature", alternate=None)

        if signature is None:
            print("Couldn't find x-hubt-signature in headers")
        else:
            elements = signature.split("=")
            signatureHash = elements[1]
            expectedHash = hmac.new(os.getenv('FACEBOOK_APP_SECRET'), request.body, digestmod='sha1').hexdigest()
            if not hmac.compare_digest(expectedHash, signatureHash):
                raise ValueError("Couldn't validate the request signature")
        
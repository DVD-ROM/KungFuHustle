from hmac import new
from django.shortcuts import render
from django.views import generic
from django.http.response import Http404, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import json 
import requests
from dotenv import load_dotenv
import os
import logging
from fb.services.graph_api import GraphApi
from fb.services.config import Config
from functools import wraps 
from fb.services.security import validate_fb_request
from fb.services.profile import Profile

class ProfileView(generic.View):
    # https://stackoverflow.com/questions/51710145/what-is-csrf-exempt/51710371
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs) 
    

    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('verify_token','')
        mode = self.request.GET.get('mode', '')
        
        if not Config.webhookUrl().startswith("https://"):
            return HttpResponse("ERROR - Need a proper API_URL in the .env file", status=200)
        
        if (mode and token):
            if (token == Config.verifyToken):
                response = HttpResponse(status=200)
                
                if (mode == "webhook" or mode == "all"):
                    Profile.setWebhook()
                    response.write(f'<p>&#9989; Set app ${Config.appId} call to ${Config.webhookUrl()}</p>')
                if (mode == "profile" or mode == "all"):
                    Profile.setThread()
                    response.write(f'<p>&#9989; Set Messenger Profile of Page ${Config.pageId}</p>')
                if (mode == "domains" or mode == "all"):
                    Profile.setWhiteListedDomains()
                    response.write(
                        f'<p>&#9989; Whitelisted domains: ${Config.whitelistedDomains}</p>'
                    )
        
                return response
            else: 
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()
            

      

                


from django.shortcuts import render
from django.views import generic
from django.http.response import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import json 
import requests
from dotenv import load_dotenv
import os
import logging
from services.config import Config
from functools import wraps 
from services.security import validate_fb_request


class Profile(generic.View):
    # https://stackoverflow.com/questions/51710145/what-is-csrf-exempt/51710371
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs) 
    
    @validate_fb_request
    def get(self, request, *args, **kwargs):
        token = self.request.GET['verify_token']
        mode = self.request.GET['mode']
        if not Config.webhookUrl().startswith("https://"):
            return HttpResponse("ERROR - Need a proper API_URL in the .env file", status=200)
        

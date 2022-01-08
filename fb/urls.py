from django.urls import path
from .views import Webhook, Profile

urlpatterns = [
	path('webhook/', Webhook.as_view()),
	path('profile/', Profile.as_view())
]
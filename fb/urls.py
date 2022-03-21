from django.urls import include, path
from fb.views.profileView import ProfileView
from fb.views.webhookView import WebhookView

urlpatterns = [
	path('webhook/', WebhookView.as_view()),
	path('profile/', ProfileView.as_view())
]

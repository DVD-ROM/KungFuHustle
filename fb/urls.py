from django.urls import path
from .views import fbView

urlpatterns = [
	path('webhook/', fbView.as_view()),
]
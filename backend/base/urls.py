from django.urls import path
from . import views

urlpatterns = [
    path('subscribe', views.createEmail, name="subscribe"),
    path('unsubscribe', views.deleteEmail, name="unsubscribe"),
    path('emails', views.getEmails, name="emails"),
]
from django.urls import path
from . import visa_views as views

urlpatterns = [
    path('subscribe', views.createEmail, name="subscribe"),
    path('unsubscribe', views.deleteEmail, name="unsubscribe"),
    path('emails', views.getEmails, name="emails"),
    path('bulletin', views.getBulletin, name="bulletin"),

]
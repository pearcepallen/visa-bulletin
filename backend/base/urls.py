from django.urls import path
from . import views

urlpatterns = [
    path('subscribe', views.addEmail, name="subscribe"),
    path('unsubscribe', views.removeEmail, name="unsubscribe"),

]
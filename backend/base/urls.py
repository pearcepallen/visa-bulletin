from django.urls import path
from . import views

urlpatterns = [
    path('', views.getBulletin, name="bulletin"),
]
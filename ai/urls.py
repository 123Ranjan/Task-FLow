from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.smart_chat, name='smart_chat'),
    path('suggestions/', views.get_suggestions, name='get_suggestions'),
]
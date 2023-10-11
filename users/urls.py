"""Module providing the users app urls."""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('railway.urls')),

]

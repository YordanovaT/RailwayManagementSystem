"""Module providing the users app urls."""
from django.urls import path, include
from . import views
urlpatterns=[
    path('', include('railway.urls')),
    path('accounts/login/', views.login_view, name='login_view'),
    path('accounts/register/', views.user_registration, name='user_registration'),
    path('user_logout/', views.user_logout, name='user_logout'),
]

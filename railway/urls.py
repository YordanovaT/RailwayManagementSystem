""" Urls for Railway system."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_lines/<int:start_station_id>/', views.ticket_lines, name='ticket_lines'),
    path('live_schedule/', views.live_schedule_departing, name='live_schedules'),
    path('live_schedule/arrivals/', views.live_schedule_arrivals, name='live_schedule_arrivals'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('edit_station/<int:station_id>/', views.edit_station, name='edit_station'),
    path('edit_train/<int:train_id>/', views.edit_train, name='edit_train')
]

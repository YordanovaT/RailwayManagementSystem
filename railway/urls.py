""" Urls for Railway system."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket_lines/<int:start_station_id>/', views.ticket_lines, name='ticket_lines'),
    path('live_schedule/', views.live_schedule_departing, name='live_schedules'),
    path('live_schedule/arrivals/', views.live_schedule_arrivals, name='live_schedule_arrivals'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('edit_station/<int:station_id>/', views.edit_station, name='edit_station'),
    path('add_station/', views.add_station, name='add_station'),
    path('delete_station/<int:pk>/', views.delete_station, name='delete_station'),
    path('edit_train/<int:train_id>/', views.edit_train, name='edit_train'),
    path('add_train/', views.add_train, name='add_train'),
    path('delete_train/<int:id>/', views.delete_train, name='delete_train')
]

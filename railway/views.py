""" Views for Railway system."""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Station, Train, Route, Ticket
from .forms import StationForm, TrainForm, BookTicketForm, UserRegisterForm
from django.utils import timezone
import random


# Create your views here.


def index(request):
    """ Retrieve the stations and trains lists
         Args:
            request: Http request
         Returns:
    """

    return render(request, 'railway/index.html', {
        'stations': Station.objects.all(),
        'trains': Train.objects.all(),
    })


def ticket_lines(request, start_station_id):
    """ Retrieve the ticket lines for the selected station from stations list
        Args:
            request: Http request
            start_station_id: Start station id
        Returns:
    """

    stations_query = Route.objects.filter(from_station=start_station_id)

    return render(request, 'railway/ticket_lines.html', {
        'ticket_lines': stations_query,
    })


def live_schedule_departing(request):
    """ Departures live schedule for stations
           Args:
               request: Http request
           Returns:
    """
    departing_time = timezone.now()
    search_query = request.GET.get('station_name')
    ticket_lines_query = Route.objects.filter(from_station_id__name=search_query,
                                              departure_time__gte=departing_time)

    return render(request, 'railway/live_schedule.html', {
        'live_schedules': ticket_lines_query,
    })


def live_schedule_arrivals(request):
    """ Arrivals live schedule for stations
           Args:
               request: Http request
           Returns:
    """
    arrival_time = timezone.now()
    search_query = request.GET.get('station_name')
    ticket_lines_query = Route.objects.filter(to_station_id__name=search_query,
                                              arrival_time__gte=arrival_time, )

    return render(request, 'railway/live_schedule_arrivals.html', {
        'live_schedules_arrivals': ticket_lines_query,
    })


@login_required
def book_ticket(request):
    """ Book a ticket view. It checks if the user is authenticated. If not - the user is redirected to the login page.
        Else the user can book a ticket.
               Args:
                   request: Http request
               Returns:
        """

    if request.user.is_authenticated:
        ticket_form = BookTicketForm()
        context = {
            'ticket_form': ticket_form
        }

        if request.method == 'POST':
            ticket_form = BookTicketForm(request.POST)

            if ticket_form.is_valid():

                seat_number = ticket_form.cleaned_data.get('seat_number')
                ticket_line = ticket_form.cleaned_data.get('ticket_line')

                max_quantity_of_tickets = ticket_line.quantity

                if max_quantity_of_tickets == 0:
                    context['max_quantity']=True
                    return render(request, 'railway/book_ticket.html', context=context)

                ticket_form.save()
                context['success'] = True

                max_quantity_of_tickets -= 1
                ticket_line.quantity = max_quantity_of_tickets
                ticket_number=Ticket().ticket_number

                ticket_line.save()

                context['ticket'] = ticket_line
                context['seat_number']=seat_number
                context['ticket_number']=ticket_number

                return render(request, 'railway/book_ticket.html', context=context)

            else:
                context['ticket_errors']=True
                return render(request, 'railway/seat_taken.html', context=context)
        else:
            departing_station_get = request.GET.get('departing_station_name')
            arrival_station_get = request.GET.get('arrival_station_name')
            date = request.GET.get('departure_time')

            ticket_form = BookTicketForm(arrival_station_name=arrival_station_get,
                                         departing_station_name=departing_station_get,
                                         departure_time=date)

        return render(request, 'railway/book_ticket.html', {
            'form': ticket_form
        })
    else:
        return render(request, 'railway/user_login.html')


def user_registration(request, form=None):
    """This function is used for user registration. """
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Congrats! You registration was successful.')
            return redirect('index')
    else:
        register_form = UserRegisterForm()
    return render(request, 'railway/user_registration.html', {'form': register_form,
                                                              'success': True})


def user_login(request):
    """This function is used for logging in user. """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong when logging in. Please try again')
            return render(request, 'railway/user_login.html', {'success': False})
    else:
        return render(request, 'railway/user_login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You logged out.')
    return redirect('index')


def edit_station(request, station_id):
    """ Edit station
        Args:
            request: Http request
            station_id: Station id
        Returns:
    """
    if request.method == 'POST':
        station = Station.objects.get(pk=station_id)
        edit_form = StationForm(request.POST, instance=station)
        if edit_form.is_valid():
            edit_form.save()

            return render(request, 'railway/edit_station.html', {
                'form': StationForm(),
                'success': True,
            })
    else:
        station = Station.objects.get(pk=station_id)
        edit_form = StationForm(instance=station)
        return render(request, 'railway/edit_station.html', {
            'form': StationForm(),
        })


def edit_train(request, train_id):
    """ Edit train
        Args:
            request: Http request
            train_id: Train id
        Returns:
    """
    if request.method == 'POST':
        train = Train.objects.get(pk=train_id)
        edit_form = TrainForm(request.POST, instance=train)
        if edit_form.is_valid():
            edit_form.save()

            return render(request, 'railway/edit_train.html', {
                'form': TrainForm(),
                'success': True,
            })
    else:
        train = Train.objects.get(pk=train_id)
        edit_form = TrainForm(instance=train)
        return render(request, 'railway/edit_train.html', {
            'form': TrainForm(),
        })

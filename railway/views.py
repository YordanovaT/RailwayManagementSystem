""" Views for Railway system."""
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Station, Train, Route, Ticket
from .forms import StationForm, TrainForm, BookTicketForm
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


def book_ticket(request):
    """ Book a ticket view. It checks if the user is authenticated. If not - the user is redirected to the login page.
        Else the user can book a ticket.
               Args:
                   request: Http request
               Returns:
        """

    context = {}

    if request.method == 'POST':
        ticket_form = BookTicketForm(request.POST)

        if ticket_form.is_valid():

            seat_number = ticket_form.cleaned_data.get('seat_number')
            ticket_line = ticket_form.cleaned_data.get('ticket_line')

            max_quantity_of_tickets = ticket_line.quantity

            if max_quantity_of_tickets == 0:
                context['max_quantity'] = True
                return render(request, 'railway/book_ticket.html', context=context)

            ticket_form.save()
            context['success'] = True

            max_quantity_of_tickets -= 1
            ticket_line.quantity = max_quantity_of_tickets
            ticket_number = Ticket().ticket_number
            if request.user.is_authenticated:
                ticket_line.save()

                context['ticket'] = ticket_line
                context['seat_number'] = seat_number
                context['ticket_number'] = ticket_number

                return render(request, 'railway/book_ticket.html', context=context)

        else:
            context['ticket_errors'] = True
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


def add_station(request):
    """ Add station
        Args:
            request: Http request
        Returns:
    """
    context = {}
    if request.POST:
        station_form = StationForm(request.POST)
        if station_form.is_valid():
            new_station_name = station_form.cleaned_data['name']
            new_station = Station(name=new_station_name)
            new_station.save()
            context['form'] = station_form
            context['success'] = True
            return redirect('index')
        else:  # not valid form
            context['form'] = station_form
    else:
        station_form = StationForm()
        context['form'] = station_form
    return render(request, 'railway/add_station.html', context)


def edit_station(request, station_id):
    """ Edit station
        Args:
            request: Http request
            station_id: Station id
        Returns:
    """
    context = {}
    if request.method == 'POST':
        station = Station.objects.get(pk=station_id)
        station_edit_form = StationForm(request.POST, instance=station)
        if station_edit_form.is_valid():
            station_edit_form.save()
            context['form'] = station_edit_form
            return redirect('index')
        else:  # not valid form
            context['form'] = station_edit_form
    else:  # GET request
        station = Station.objects.get(pk=station_id)
        station_edit_form = StationForm(instance=station)
        context['form'] = station_edit_form
    return render(request, 'railway/edit_station.html', context)


def delete_station(request, pk):
    """ Delete station
            Args:
                request: Http request
                station_id: Station id
            Returns:
        """

    if request.method == 'POST':
        station = Station.objects.get(pk=pk)
        station.delete()
    return redirect('index')


def add_train(request):
    """ Add station
        Args:
            request: Http request
        Returns:
    """
    context = {}
    if request.POST:
        train_form = TrainForm(request.POST)
        if train_form.is_valid():
            new_train_name = train_form.cleaned_data['name']
            train_type_select = train_form.cleaned_data['train_type']
            new_station = Train(name=new_train_name, train_type=train_type_select)
            new_station.save()
            context['form'] = train_form
            context['success'] = True
            return redirect('index')
        else:  # not valid form
            context['form'] = train_form
    else:
        train_form = TrainForm()
        context['form'] = train_form
    return render(request, 'railway/add_train.html', context)


def edit_train(request, train_id):
    """ Edit train
        Args:
            request: Http request
            train_id: Train id
        Returns:
    """
    context = {}
    if request.method == 'POST':
        train = Train.objects.get(pk=train_id)
        train_edit_form = TrainForm(request.POST, instance=train)
        if train_edit_form.is_valid():
            train_edit_form.save()
            context['form'] = train_edit_form
            return redirect('index')
        else:  # not valid form
            context['form'] = train_edit_form
    else:  # GET request
        train = Train.objects.get(pk=train_id)
        train_edit_form = TrainForm(instance=train)
        context['form'] = train_edit_form
    return render(request, 'railway/edit_train.html', context)


def delete_train(request, id):
    """ Delete train
            Args:
                request: Http request
                id: Train id
            Returns:
        """

    if request.method == 'POST':
        train = Train.objects.get(pk=id)
        train.delete()
    return redirect('index')

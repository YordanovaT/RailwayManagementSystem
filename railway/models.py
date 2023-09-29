""" Models for Railway system."""

from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from django.utils import timezone


# Create your models here.

class Train(models.Model):
    """ Model for the train."""

    class TrainType(models.TextChoices):
        FASTTRAIN = 'BV', _('Fast Train')
        SLOWTRAIN = 'PV', _('Slow Train')
        VERYFASTTRAIN = 'UBV', _('Very Fast Train')

    name = models.CharField(max_length=10, unique=True)
    train_type = models.CharField(
        max_length=5,
        choices=TrainType.choices,
    )

    def __str__(self):
        return f'Train: {self.name}'


class Station(models.Model):
    """ Model for the station."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'Station: {self.name}'


class Distance(models.Model):
    """ Model for the distance between stations. """

    distance = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.distance} km'


class Delay(models.Model):
    """ Model for the delay."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delay = models.IntegerField()

    def __str__(self):
        return f'{self.delay} min'


class Route(models.Model):
    """ Model for the route."""

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.PROTECT)
    from_station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='from_station')  # start station
    to_station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='to_station')  # final station
    distance = models.ForeignKey(Distance, on_delete=models.PROTECT)
    delay = models.ForeignKey(Delay, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'Route:  from {self.from_station}, to {self.to_station}, {self.departure_time}, {self.arrival_time}'


class TicketLine(models.Model):
    """ Model for the ticket line."""

    route = models.ManyToManyField(Route)
    price = models.FloatField()
    quantity = models.IntegerField()  # how many tickets will the ticket line have

    def __str__(self):
        stations = []
        for route in self.route.all().order_by('departure_time'):
            stations.append(f' from: {route.from_station} - to: {route.to_station}, Departing: {route.departure_time}')

        return f'{"; ".join(stations)}'


class Ticket(models.Model):
    """ Model for the ticket line."""

    seat_number = models.PositiveIntegerField(unique=True)
    ticket_line = models.ForeignKey(TicketLine, on_delete=models.PROTECT)
    ticket_number = models.PositiveIntegerField(blank=True, default=random.randrange(10000))

    def __str__(self):
        return f'Ticket Number:{self.ticket_number} , Seat Number:{self.seat_number} , {self.ticket_line}'

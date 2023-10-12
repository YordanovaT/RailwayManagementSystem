from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Station, Train, TicketLine, Ticket


class StationForm(forms.ModelForm):
    """ Django form which will be used to edit stations. """

    class Meta:
        model = Station
        fields = ['name']
        labels = {
            'name': 'Station Name',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TrainForm(forms.ModelForm):
    """ Django form which will be used to add and edit trains. """
    class Meta:
        model = Train
        fields = ['name', 'train_type']
        labels = {
            'name': 'Train Name',
            'train_type': 'Train Type',
        }


class MyModelChoiceField(forms.ModelChoiceField):
    """" This class is used in the book ticket functionality"""

    def label_from_instance(self, obj):
        """"Function to return information about the available ticket lines"""

        return f'{obj.__str__()}'


class BookTicketForm(forms.ModelForm):
    """ Django form which will be used to book a ticket. """

    def __init__(self, *args, **kwargs):
        """ Constructor method which helps to enter departing and arrival station search
             and returns the available ticket lines.
        """
        self.departing_station_name = kwargs.pop('departing_station_name', None)
        self.arrival_station_name = kwargs.pop('arrival_station_name', None)
        self.departing_time = kwargs.pop('departure_time', None)

        super(BookTicketForm, self).__init__(*args, **kwargs)
        if self.departing_station_name and self.arrival_station_name:
            queryset = TicketLine.objects.filter(route__from_station_id__name__in=[self.departing_station_name],
                                                 route__departure_time__gte=self.departing_time)
            for line in queryset.all():
                flag = False
                for route in line.route.all():
                    if self.arrival_station_name == route.to_station.name :
                        flag = True
                if not flag:
                    queryset = queryset.exclude(pk=line.pk)

            self.fields['ticket_line'] = MyModelChoiceField(queryset=queryset, widget=forms.RadioSelect)
        elif not args:
            queryset = TicketLine.objects.none()

            self.fields['ticket_line'] = MyModelChoiceField(queryset=queryset, widget=forms.RadioSelect)

    class Meta:
        model = Ticket
        fields = ('seat_number', 'ticket_line')



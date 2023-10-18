"""Django admin module"""

from django.contrib import admin
from .models import Train, Station, Route, Ticket, TicketLine, Distance, Delay

# Register your models here.
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(TicketLine)
admin.site.register(Distance)


@admin.register(Delay)
class DelayAdmin(admin.ModelAdmin):
    """Class customizing delay for admin"""

    readonly_fields = ['created_at', 'updated_at']

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(TicketLine)
admin.site.register(Distance)


@admin.register(Delay)
class DelayAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


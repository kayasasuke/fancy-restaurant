from django.contrib import admin

from .models import Customer, Reservation, Table, TimeSlot

admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(TimeSlot)
admin.site.register(Reservation)

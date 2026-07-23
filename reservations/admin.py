from django.contrib import admin

from .models import Reservation, Table, TimeSlot


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity", "is_active")
    list_filter = ("is_active", "capacity")
    ordering = ("capacity", "table_number")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("start_time", "duration_minutes", "is_active")
    list_filter = ("is_active",)
    ordering = ("start_time",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "reservation_date",
        "time_slot",
        "guest_count",
        "table",
        "status",
    )
    list_filter = ("reservation_date", "time_slot", "status")
    search_fields = ("customer_name", "user__username", "user__email")
    ordering = ("reservation_date", "time_slot__start_time", "table__table_number")

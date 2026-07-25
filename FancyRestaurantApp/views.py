from datetime import date, time

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import Customer, Reservation, Table, TimeSlot


def home(request):
    return render(request, "FancyRestaurantApp/home.html")


def table_list(request):
    tables = Table.objects.order_by("capacity", "table_number")
    return render(request, "FancyRestaurantApp/table_list.html", {"tables": tables})


def time_slot_list(request):
    slots = TimeSlot.objects.order_by("start_time")
    return render(request, "FancyRestaurantApp/time_slot_list.html", {"slots": slots})


def reservation_form(request):
    return render(request, "FancyRestaurantApp/reservation_form.html")


def create_sample_reservation(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    slot = TimeSlot.objects.filter(start_time=time(18, 0)).first()
    if slot is None:
        return HttpResponse("The sample time slot is unavailable.", status=409)
    reservation_date = date(2026, 8, 1)

    occupied_table_ids = Reservation.objects.filter(
        reservation_date=reservation_date,
        time_slot=slot,
    ).values_list("table_id", flat=True)

    table = (
        Table.objects.filter(capacity__gte=2)
        .exclude(id__in=occupied_table_ids)
        .order_by("capacity", "table_number")
        .first()
    )
    if table is None:
        return HttpResponse("No suitable table is available.", status=409)

    customer = Customer.objects.filter(name="Alice", login="").first()
    if customer is None:
        customer = Customer.objects.create(name="Alice", login="", password="")
    reservation = Reservation.objects.create(
        customer=customer,
        reservation_date=reservation_date,
        time_slot=slot,
        guest_count=2,
        table=table,
    )
    return redirect("reservation-detail", reservation_id=reservation.id)


def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.select_related("customer", "time_slot", "table"),
        pk=reservation_id,
    )
    return render(
        request,
        "FancyRestaurantApp/reservation_detail.html",
        {"reservation": reservation},
    )

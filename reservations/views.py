from datetime import date, time

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.middleware.csrf import get_token
from django.utils.html import escape

from .models import Reservation, Table, TimeSlot


def home(request):
    return HttpResponse("""
        <h1>Fancy Restaurant Reservations</h1>
        <p>Welcome to the reservation app.</p>
        <ul>
            <li><a href="/tables/">View tables</a></li>
            <li><a href="/time-slots/">View time slots</a></li>
            <li><a href="/reservations/new/">Start a reservation</a></li>
        </ul>
        """)


def table_list(request):
    tables = Table.objects.filter(is_active=True)
    rows = [
        f"<li>Table {table.table_number}: {table.capacity} seats</li>"
        for table in tables
    ]
    content = "<h1>Active Tables</h1><ul>{}</ul>".format("".join(rows))
    return HttpResponse(content)


def time_slot_list(request):
    slots = TimeSlot.objects.filter(is_active=True)
    rows = [
        f"<li>{slot.start_time.strftime('%H:%M')} for {slot.duration_minutes} minutes</li>"
        for slot in slots
    ]
    content = "<h1>Active Time Slots</h1><ul>{}</ul>".format("".join(rows))
    return HttpResponse(content)


def reservation_form(request):
    csrf_token = get_token(request)
    return HttpResponse(f"""
        <h1>Reservation Form</h1>
        <p>This is a placeholder form page for Exercise 6.</p>
        <p>Current sample values: Alice, 2 guests, 2026-08-01, 18:00.</p>
        <form method="post" action="/reservations/sample-create/">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <button type="submit">Create the sample reservation</button>
        </form>
        """)


def create_sample_reservation(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    slot, _created = TimeSlot.objects.get_or_create(
        start_time=time(18, 0),
        defaults={"duration_minutes": 90},
    )
    reservation_date = date(2026, 8, 1)

    occupied_table_ids = Reservation.objects.filter(
        reservation_date=reservation_date,
        time_slot=slot,
        status__in=[Reservation.Status.PENDING, Reservation.Status.CONFIRMED],
    ).values_list("table_id", flat=True)

    table = (
        Table.objects.filter(is_active=True, capacity__gte=2)
        .exclude(id__in=occupied_table_ids)
        .first()
    )
    if table is None:
        latest_table = Table.objects.order_by("-table_number").first()
        table_number = latest_table.table_number + 1 if latest_table else 1
        table = Table.objects.create(table_number=table_number, capacity=2)

    reservation = Reservation.objects.create(
        customer_name="Alice",
        reservation_date=reservation_date,
        time_slot=slot,
        guest_count=2,
        table=table,
    )
    return redirect("reservation-detail", reservation_id=reservation.id)


def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.select_related("time_slot", "table"),
        pk=reservation_id,
    )
    return HttpResponse(f"""
        <h1>Reservation Detail</h1>
        <p>Customer: {escape(reservation.customer_name)}</p>
        <p>Date: {reservation.reservation_date}</p>
        <p>Time: {reservation.time_slot.start_time.strftime('%H:%M')}</p>
        <p>Guests: {reservation.guest_count}</p>
        <p>Table: {reservation.table.table_number}</p>
        <p>Status: {reservation.get_status_display()}</p>
        <p><a href="{reverse('home')}">Back home</a></p>
        """)

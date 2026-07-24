from datetime import date, time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Reservation, Table, TimeSlot


def home(request):
    return HttpResponse("""
        <h1>Fancy Restaurant Reservations</h1>
        <p>Welcome to the reservation app.</p>
        <ul>
            <li><a href="/tables/">View tables</a></li>
            <li><a href="/time-slots/">View time slots</a></li>
            <li><a href="/reservations/new/">Start a reservation</a></li>
            <li><a href="/reservations/sample-create/">Create sample reservation</a></li>
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
    return HttpResponse("""
        <h1>Reservation Form</h1>
        <p>This is a placeholder form page for Exercise 6.</p>
        <p>Current sample values: Alice, 2 guests, 2026-08-01, 18:00.</p>
        <p><a href="/reservations/sample-create/">Create the sample reservation</a></p>
        """)


def create_sample_reservation(request):
    table, _created = Table.objects.get_or_create(
        table_number=1,
        defaults={"capacity": 2},
    )
    slot, _created = TimeSlot.objects.get_or_create(
        start_time=time(18, 0),
        defaults={"duration_minutes": 90},
    )
    reservation_date = date(2026, 8, 1)

    Reservation.objects.filter(
        customer_name="Alice",
        reservation_date=reservation_date,
        time_slot=slot,
        table=table,
    ).update(status=Reservation.Status.CANCELLED)

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
        <p>Customer: {reservation.customer_name}</p>
        <p>Date: {reservation.reservation_date}</p>
        <p>Time: {reservation.time_slot.start_time.strftime('%H:%M')}</p>
        <p>Guests: {reservation.guest_count}</p>
        <p>Table: {reservation.table.table_number}</p>
        <p>Status: {reservation.get_status_display()}</p>
        <p><a href="{reverse('home')}">Back home</a></p>
        """)

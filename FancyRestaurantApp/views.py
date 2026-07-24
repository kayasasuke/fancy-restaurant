from datetime import date, time

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.middleware.csrf import get_token
from django.utils.html import escape

from .models import Customer, Reservation, Table, TimeSlot


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
    tables = Table.objects.all()
    rows = [
        f"<li>Table {table.table_number}: {table.capacity} seats</li>"
        for table in tables
    ]
    content = f"<h1>Restaurant Tables</h1><ul>{''.join(rows)}</ul>"
    return HttpResponse(content)


def time_slot_list(request):
    slots = TimeSlot.objects.all()
    rows = [f"<li>{slot.start_time.strftime('%H:%M')}</li>" for slot in slots]
    content = f"<h1>Reservation Time Slots</h1><ul>{''.join(rows)}</ul>"
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
    return HttpResponse(f"""
        <h1>Reservation Detail</h1>
        <p>Customer: {escape(reservation.customer.name)}</p>
        <p>Date: {reservation.reservation_date}</p>
        <p>Time: {reservation.time_slot.start_time.strftime('%H:%M')}</p>
        <p>Guests: {reservation.guest_count}</p>
        <p>Table: {reservation.table.table_number}</p>
        <p><a href="{reverse('home')}">Back home</a></p>
        """)

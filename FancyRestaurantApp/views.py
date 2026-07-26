from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError, transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvailabilityForm, LoginForm, RegistrationForm, ReservationForm
from .models import Customer, Reservation, Table, TimeSlot


def home(request):
    return render(request, "FancyRestaurantApp/home.html")


def authenticated_customer(request):
    customer_login = request.session.get("authorized_customer_login")
    if not customer_login:
        return None

    customer = Customer.objects.filter(login=customer_login).first()
    if customer is None:
        request.session.pop("authorized_customer_login", None)
    return customer


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()
    if request.method == "POST" and form.is_valid():
        customer_login = form.cleaned_data["login"]
        try:
            with transaction.atomic():
                Customer.objects.create(
                    name=form.cleaned_data["name"],
                    login=customer_login,
                    password=make_password(form.cleaned_data["password"]),
                )
        except IntegrityError:
            form.add_error("login", "This login is already in use.")
        else:
            request.session.cycle_key()
            request.session["authorized_customer_login"] = customer_login
            return redirect("home")

    return render(
        request,
        "FancyRestaurantApp/authentication_form.html",
        {"form": form, "heading": "Create account"},
    )


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    if request.method == "POST" and form.is_valid():
        customer = Customer.objects.filter(login=form.cleaned_data["login"]).first()
        if customer is None or not check_password(
            form.cleaned_data["password"], customer.password
        ):
            form.add_error(None, "Invalid login or password.")
        else:
            request.session.cycle_key()
            request.session["authorized_customer_login"] = customer.login
            return redirect("home")

    return render(
        request,
        "FancyRestaurantApp/authentication_form.html",
        {"form": form, "heading": "Log in"},
    )


def logout(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    request.session.flush()
    return redirect("home")


def table_list(request):
    tables = Table.objects.order_by("capacity", "table_number")
    return render(request, "FancyRestaurantApp/table_list.html", {"tables": tables})


def time_slot_list(request):
    slots = TimeSlot.objects.order_by("start_time")
    return render(request, "FancyRestaurantApp/time_slot_list.html", {"slots": slots})


def find_available_table(reservation_date, time_slot, guest_count):
    occupied_table_ids = Reservation.objects.filter(
        reservation_date=reservation_date,
        time_slot=time_slot,
    ).values_list("table_id", flat=True)
    return (
        Table.objects.filter(capacity__gte=guest_count)
        .exclude(id__in=occupied_table_ids)
        .order_by("capacity", "table_number")
        .first()
    )


def reservation_form(request):
    time_slots = TimeSlot.objects.order_by("start_time")
    customer = authenticated_customer(request)
    if request.method == "POST":
        form = ReservationForm(
            request.POST,
            time_slots=time_slots,
            customer=customer,
        )
    else:
        form = ReservationForm(time_slots=time_slots, customer=customer)

    if request.method == "POST" and form.is_valid():
        reservation_date = form.cleaned_data["reservation_date"]
        time_slot = TimeSlot.objects.get(pk=form.cleaned_data["time_slot"])
        guest_count = form.cleaned_data["guest_count"]
        table = find_available_table(reservation_date, time_slot, guest_count)
        if table is None:
            form.add_error(None, "No suitable table is available.")
        else:
            if customer is None:
                customer = Customer.objects.create(
                    name=form.cleaned_data["customer_name"],
                    login="",
                    password="",
                )
            reservation = Reservation.objects.create(
                customer=customer,
                reservation_date=reservation_date,
                time_slot=time_slot,
                guest_count=guest_count,
                table=table,
            )
            return redirect("reservation-detail", reservation_id=reservation.id)

    return render(request, "FancyRestaurantApp/reservation_form.html", {"form": form})


def my_reservations(request):
    customer = authenticated_customer(request)
    if customer is None:
        return redirect("login")

    reservations = (
        Reservation.objects.filter(customer=customer)
        .select_related("table", "time_slot")
        .order_by("reservation_date", "time_slot__start_time")
    )
    return render(
        request,
        "FancyRestaurantApp/my_reservations.html",
        {"reservations": reservations},
    )


def reservation_availability(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    time_slots = TimeSlot.objects.order_by("start_time")
    form = AvailabilityForm(request.POST, time_slots=time_slots)
    if not form.is_valid():
        return render(request, "FancyRestaurantApp/availability_result.html")

    table = find_available_table(
        form.cleaned_data["reservation_date"],
        TimeSlot.objects.get(pk=form.cleaned_data["time_slot"]),
        form.cleaned_data["guest_count"],
    )
    return render(
        request,
        "FancyRestaurantApp/availability_result.html",
        {"table": table, "unavailable": table is None},
    )


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

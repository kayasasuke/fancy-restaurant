from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservationForm
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
    time_slots = TimeSlot.objects.order_by("start_time")
    if request.method == "POST":
        form = ReservationForm(request.POST, time_slots=time_slots)
    else:
        form = ReservationForm(time_slots=time_slots)

    if request.method == "POST" and form.is_valid():
        reservation_date = form.cleaned_data["reservation_date"]
        time_slot = TimeSlot.objects.get(pk=form.cleaned_data["time_slot"])
        guest_count = form.cleaned_data["guest_count"]
        occupied_table_ids = Reservation.objects.filter(
            reservation_date=reservation_date,
            time_slot=time_slot,
        ).values_list("table_id", flat=True)
        table = (
            Table.objects.filter(capacity__gte=guest_count)
            .exclude(id__in=occupied_table_ids)
            .order_by("capacity", "table_number")
            .first()
        )
        if table is None:
            form.add_error(None, "No suitable table is available.")
        else:
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

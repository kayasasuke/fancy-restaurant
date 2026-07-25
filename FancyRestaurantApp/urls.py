from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tables/", views.table_list, name="table-list"),
    path("time-slots/", views.time_slot_list, name="time-slot-list"),
    path("reservations/new/", views.reservation_form, name="reservation-form"),
    path(
        "reservations/availability/",
        views.reservation_availability,
        name="reservation-availability",
    ),
    path(
        "reservations/<int:reservation_id>/",
        views.reservation_detail,
        name="reservation-detail",
    ),
]

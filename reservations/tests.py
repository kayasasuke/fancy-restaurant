from datetime import date, time

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Reservation, Table, TimeSlot


class ReservationModelTests(TestCase):
    def test_table_string_includes_number_and_capacity(self):
        table = Table.objects.create(table_number=3, capacity=4)

        self.assertEqual(str(table), "Table 3 (4 seats)")

    def test_time_slot_string_uses_start_time(self):
        slot = TimeSlot.objects.create(start_time=time(18, 30))

        self.assertEqual(str(slot), "18:30")

    def test_active_time_slots_cannot_overlap(self):
        TimeSlot.objects.create(start_time=time(18, 0), duration_minutes=90)

        with self.assertRaises(ValidationError):
            TimeSlot.objects.create(start_time=time(19, 0), duration_minutes=90)

    def test_active_time_slot_cannot_extend_past_midnight(self):
        with self.assertRaises(ValidationError):
            TimeSlot.objects.create(start_time=time(23, 30), duration_minutes=90)

    def test_reservation_string_identifies_booking(self):
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(19, 0))
        reservation = Reservation.objects.create(
            customer_name="Alice",
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        self.assertEqual(
            str(reservation),
            "Alice on 2026-08-01 at 19:00 - Table 1 (2 seats)",
        )

    def test_tables_order_by_capacity_then_number(self):
        larger_table = Table.objects.create(table_number=1, capacity=6)
        smaller_late_table = Table.objects.create(table_number=5, capacity=2)
        smaller_early_table = Table.objects.create(table_number=2, capacity=2)

        self.assertEqual(
            list(Table.objects.all()),
            [smaller_early_table, smaller_late_table, larger_table],
        )

    def test_same_table_cannot_be_reserved_twice_for_same_slot(self):
        table = Table.objects.create(table_number=1, capacity=4)
        slot = TimeSlot.objects.create(start_time=time(18, 0))
        reservation_date = date(2026, 8, 1)
        Reservation.objects.create(
            customer_name="Alice",
            reservation_date=reservation_date,
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        with self.assertRaises(IntegrityError):
            Reservation.objects.create(
                customer_name="Bob",
                reservation_date=reservation_date,
                time_slot=slot,
                guest_count=2,
                table=table,
            )

    def test_cancelled_reservation_does_not_block_same_table_slot(self):
        table = Table.objects.create(table_number=1, capacity=4)
        slot = TimeSlot.objects.create(start_time=time(18, 0))
        reservation_date = date(2026, 8, 1)
        Reservation.objects.create(
            customer_name="Alice",
            reservation_date=reservation_date,
            time_slot=slot,
            guest_count=2,
            table=table,
            status=Reservation.Status.CANCELLED,
        )

        reservation = Reservation.objects.create(
            customer_name="Bob",
            reservation_date=reservation_date,
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        self.assertEqual(reservation.customer_name, "Bob")

    def test_reservation_guest_count_cannot_exceed_table_capacity(self):
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(18, 0))
        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                customer_name="Alice",
                reservation_date=date(2026, 8, 1),
                time_slot=slot,
                guest_count=3,
                table=table,
            )


class ReservationViewTests(TestCase):
    def test_home_page_is_callable(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fancy Restaurant Reservations")
        self.assertContains(response, "/tables/")

    def test_table_list_shows_active_tables(self):
        Table.objects.create(table_number=3, capacity=4)
        Table.objects.create(table_number=9, capacity=8, is_active=False)

        response = self.client.get(reverse("table-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Table 3: 4 seats")
        self.assertNotContains(response, "Table 9")

    def test_time_slot_list_shows_active_slots(self):
        TimeSlot.objects.create(start_time=time(18, 0), duration_minutes=90)
        TimeSlot.objects.create(
            start_time=time(20, 0),
            duration_minutes=90,
            is_active=False,
        )

        response = self.client.get(reverse("time-slot-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18:00 for 90 minutes")
        self.assertNotContains(response, "20:00")

    def test_reservation_form_placeholder_is_callable(self):
        response = self.client.get(reverse("reservation-form"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reservation Form")
        self.assertContains(response, "Alice, 2 guests, 2026-08-01, 18:00")

    def test_sample_reservation_create_redirects_to_detail(self):
        response = self.client.get(reverse("reservation-sample-create"))

        reservation = Reservation.objects.get(customer_name="Alice")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("reservation-detail", args=[reservation.id]),
        )

    def test_reservation_detail_shows_existing_reservation(self):
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(18, 0), duration_minutes=90)
        reservation = Reservation.objects.create(
            customer_name="Alice",
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        response = self.client.get(reverse("reservation-detail", args=[reservation.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customer: Alice")
        self.assertContains(response, "Date: 2026-08-01")
        self.assertContains(response, "Table: 1")

    def test_reservation_detail_returns_404_for_missing_reservation(self):
        response = self.client.get(reverse("reservation-detail", args=[999]))

        self.assertEqual(response.status_code, 404)

from datetime import date, time
from importlib import import_module

from django.test import TestCase
from django.urls import reverse

from .models import Customer, Reservation, Table, TimeSlot


class ReservationModelTests(TestCase):
    def test_data_migration_rejects_customer_names_longer_than_twenty_characters(self):
        migration = import_module(
            "FancyRestaurantApp.migrations.0003_simplify_reservation_schema"
        )

        with self.assertRaises(RuntimeError):
            migration.validated_customer_name("A" * 21)

    def test_customer_string_uses_name(self):
        customer = Customer.objects.create(name="Alice", login="alice", password="hash")

        self.assertEqual(str(customer), "Alice")

    def test_table_string_includes_number_and_capacity(self):
        table = Table.objects.create(table_number=3, capacity=4)

        self.assertEqual(str(table), "Table 3 (4 seats)")

    def test_time_slot_string_uses_start_time(self):
        slot = TimeSlot.objects.create(start_time=time(18, 30))

        self.assertEqual(str(slot), "18:30")

    def test_reservation_string_identifies_booking(self):
        customer = Customer.objects.create(name="Alice", login="alice", password="hash")
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(19, 0))
        reservation = Reservation.objects.create(
            customer=customer,
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        self.assertEqual(str(reservation), "Alice -> Table 1 (2 seats) (2026-08-01)")


class ReservationViewTests(TestCase):
    def create_sample_slot(self):
        return TimeSlot.objects.create(start_time=time(18, 0))

    def test_home_page_is_callable(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/home.html")
        self.assertContains(response, "Fancy Restaurant Reservations")
        self.assertContains(response, "Fancy Restaurant Reservation System")

    def test_table_list_shows_tables(self):
        Table.objects.create(table_number=3, capacity=4)

        response = self.client.get(reverse("table-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/table_list.html")
        self.assertContains(response, "Table 3: 4 seats")

    def test_time_slot_list_shows_slots(self):
        TimeSlot.objects.create(start_time=time(18, 0))

        response = self.client.get(reverse("time-slot-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/time_slot_list.html")
        self.assertContains(response, "18:00")

    def test_reservation_form_placeholder_is_callable(self):
        response = self.client.get(reverse("reservation-form"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/reservation_form.html")
        self.assertContains(response, "Reservation Form")
        self.assertContains(response, 'method="post"')

    def test_sample_reservation_create_rejects_get(self):
        response = self.client.get(reverse("reservation-sample-create"))

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Reservation.objects.exists())

    def test_sample_reservation_create_redirects_to_detail_on_post(self):
        Table.objects.create(table_number=1, capacity=2)
        self.create_sample_slot()

        response = self.client.post(reverse("reservation-sample-create"))

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("reservation-detail", args=[reservation.id]),
        )

    def test_sample_reservation_create_uses_smallest_suitable_table(self):
        Table.objects.create(table_number=1, capacity=4)
        suitable_table = Table.objects.create(table_number=2, capacity=2)
        self.create_sample_slot()

        self.client.post(reverse("reservation-sample-create"))

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(reservation.table, suitable_table)

    def test_sample_reservation_create_allows_existing_duplicate_guest_names(self):
        Customer.objects.create(name="Alice", login="", password="")
        Customer.objects.create(name="Alice", login="", password="")
        Table.objects.create(table_number=1, capacity=2)
        self.create_sample_slot()

        response = self.client.post(reverse("reservation-sample-create"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_sample_reservation_create_skips_already_reserved_table(self):
        reserved_table = Table.objects.create(table_number=1, capacity=2)
        available_table = Table.objects.create(table_number=2, capacity=2)
        slot = self.create_sample_slot()
        customer = Customer.objects.create(name="Bob", login="bob", password="hash")
        Reservation.objects.create(
            customer=customer,
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=reserved_table,
        )

        self.client.post(reverse("reservation-sample-create"))

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(reservation.table, available_table)

    def test_sample_reservation_create_does_not_create_table_when_full(self):
        self.create_sample_slot()

        response = self.client.post(reverse("reservation-sample-create"))

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Table.objects.count(), 0)
        self.assertFalse(Reservation.objects.exists())

    def test_reservation_detail_shows_existing_reservation(self):
        customer = Customer.objects.create(name="Alice", login="alice", password="hash")
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(18, 0))
        reservation = Reservation.objects.create(
            customer=customer,
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        response = self.client.get(reverse("reservation-detail", args=[reservation.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/reservation_detail.html")
        self.assertContains(response, "Customer: Alice")
        self.assertContains(response, "Date: 2026-08-01")
        self.assertContains(response, "Table: 1")

    def test_reservation_detail_escapes_customer_name(self):
        customer = Customer.objects.create(
            name="<script>alert('xss')</script>",
            login="alice",
            password="hash",
        )
        table = Table.objects.create(table_number=1, capacity=2)
        slot = TimeSlot.objects.create(start_time=time(18, 0))
        reservation = Reservation.objects.create(
            customer=customer,
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )

        response = self.client.get(reverse("reservation-detail", args=[reservation.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;",
        )
        self.assertNotContains(response, "<script>alert('xss')</script>")

    def test_reservation_detail_returns_404_for_missing_reservation(self):
        response = self.client.get(reverse("reservation-detail", args=[999]))

        self.assertEqual(response.status_code, 404)

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

    def test_reservation_form_displays_input_fields(self):
        slot = self.create_sample_slot()

        response = self.client.get(reverse("reservation-form"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/reservation_form.html")
        self.assertContains(response, "Reservation Form")
        self.assertContains(response, 'name="customer_name"')
        self.assertContains(response, 'name="guest_count"')
        self.assertContains(response, 'name="reservation_date"')
        self.assertContains(response, f'value="{slot.id}"')

    def test_reservation_form_creates_reservation_and_redirects(self):
        Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("reservation-detail", args=[reservation.id]),
        )

    def test_reservation_form_uses_smallest_suitable_table(self):
        Table.objects.create(table_number=1, capacity=4)
        suitable_table = Table.objects.create(table_number=2, capacity=2)
        slot = self.create_sample_slot()

        self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(reservation.table, suitable_table)

    def test_reservation_form_rejects_invalid_input_without_creating_records(self):
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 0,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Ensure this value is greater than or equal to 1."
        )
        self.assertFalse(Customer.objects.exists())
        self.assertFalse(Reservation.objects.exists())

    def test_reservation_form_shows_required_errors_for_an_empty_post(self):
        response = self.client.post(reverse("reservation-form"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.", count=4)
        self.assertFalse(Customer.objects.exists())
        self.assertFalse(Reservation.objects.exists())

    def test_reservation_form_skips_already_reserved_table(self):
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

        self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        reservation = Reservation.objects.get(customer__name="Alice")
        self.assertEqual(reservation.table, available_table)

    def test_reservation_form_shows_error_when_no_suitable_table_exists(self):
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No suitable table is available.")
        self.assertEqual(Table.objects.count(), 0)
        self.assertFalse(Customer.objects.exists())
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

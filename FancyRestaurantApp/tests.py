from datetime import date, datetime, time, timezone
from importlib import import_module
from unittest.mock import patch

from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .models import Customer, Reservation, Table, TimeSlot


class ReservationModelTests(TestCase):
    def test_initial_restaurant_data_fixture_loads_tables_and_time_slots(self):
        call_command("loaddata", "initial_restaurant_data", verbosity=0)
        call_command("loaddata", "initial_restaurant_data", verbosity=0)

        self.assertEqual(Table.objects.filter(capacity=2).count(), 4)
        self.assertEqual(Table.objects.filter(capacity=4).count(), 6)
        self.assertEqual(Table.objects.filter(capacity=6).count(), 6)
        self.assertEqual(TimeSlot.objects.count(), 11)
        self.assertTrue(TimeSlot.objects.filter(start_time=time(12, 0)).exists())
        self.assertTrue(TimeSlot.objects.filter(start_time=time(22, 0)).exists())

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


class CustomerAuthenticationTests(TestCase):

    def test_home_page_is_callable(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/home.html")
        self.assertContains(response, "Fancy Restaurant Reservations")
        self.assertContains(response, "Fancy Restaurant Reservation System")
        self.assertContains(
            response,
            'name="viewport" content="width=device-width, initial-scale=1"',
        )
        self.assertContains(response, "FancyRestaurantApp/style.css")
        self.assertContains(response, "FancyRestaurantApp/htmx.min.js")

    def test_navigation_hides_internal_table_and_time_slot_lists(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, 'href="/tables/"')
        self.assertNotContains(response, 'href="/time-slots/"')

    def test_registration_creates_hashed_customer_and_authenticates_session(self):
        session = self.client.session
        session["visitor"] = "anonymous"
        session.save()
        previous_session_key = session.session_key

        response = self.client.post(
            reverse("registration"),
            {
                "name": "Alice",
                "login": "alice",
                "password": "secret-password",
                "password_confirmation": "secret-password",
            },
        )

        customer = Customer.objects.get(login="alice")
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(check_password("secret-password", customer.password))
        self.assertNotEqual(self.client.session.session_key, previous_session_key)
        self.assertEqual(
            self.client.session["authorized_customer_login"],
            "alice",
        )

    def test_registration_rejects_duplicate_login_and_mismatched_passwords(self):
        Customer.objects.create(
            name="Alice",
            login="alice",
            password=make_password("secret-password"),
        )

        duplicate_response = self.client.post(
            reverse("registration"),
            {
                "name": "Another Alice",
                "login": "alice",
                "password": "secret-password",
                "password_confirmation": "secret-password",
            },
        )
        mismatch_response = self.client.post(
            reverse("registration"),
            {
                "name": "Bob",
                "login": "bob",
                "password": "secret-password",
                "password_confirmation": "different-password",
            },
        )

        self.assertEqual(duplicate_response.status_code, 200)
        self.assertContains(duplicate_response, "This login is already in use.")
        self.assertEqual(mismatch_response.status_code, 200)
        self.assertContains(mismatch_response, "Passwords do not match.")
        self.assertEqual(Customer.objects.count(), 1)

    def test_registration_applies_password_validation_and_required_errors(self):
        weak_password_response = self.client.post(
            reverse("registration"),
            {
                "name": "Alice",
                "login": "alice",
                "password": "short",
                "password_confirmation": "short",
            },
        )
        empty_response = self.client.post(reverse("registration"))

        self.assertEqual(weak_password_response.status_code, 200)
        self.assertContains(weak_password_response, "This password is too short.")
        self.assertEqual(empty_response.status_code, 200)
        self.assertContains(empty_response, "This field is required.", count=4)
        self.assertFalse(Customer.objects.exists())

    def test_login_accepts_valid_credentials_and_rejects_invalid_credentials(self):
        Customer.objects.create(
            name="Alice",
            login="alice",
            password=make_password("secret-password"),
        )

        session = self.client.session
        session["visitor"] = "anonymous"
        session.save()
        previous_session_key = session.session_key

        invalid_response = self.client.post(
            reverse("login"),
            {"login": "alice", "password": "incorrect-password"},
        )
        valid_response = self.client.post(
            reverse("login"),
            {"login": "alice", "password": "secret-password"},
        )

        self.assertEqual(invalid_response.status_code, 200)
        self.assertContains(invalid_response, "Invalid login or password.")
        self.assertRedirects(valid_response, reverse("home"))
        self.assertNotEqual(self.client.session.session_key, previous_session_key)
        self.assertEqual(
            self.client.session["authorized_customer_login"],
            "alice",
        )

    def test_login_shows_required_errors_for_empty_post(self):
        response = self.client.post(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.", count=2)

    def test_logout_clears_authenticated_session(self):
        session = self.client.session
        session["authorized_customer_login"] = "alice"
        session.save()

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("authorized_customer_login", self.client.session)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)

    def test_authentication_forms_reject_posts_without_csrf_token(self):
        client = Client(enforce_csrf_checks=True)

        registration_response = client.post(
            reverse("registration"),
            {
                "name": "Alice",
                "login": "alice",
                "password": "secret-password",
                "password_confirmation": "secret-password",
            },
        )
        login_response = client.post(
            reverse("login"),
            {"login": "alice", "password": "secret-password"},
        )
        logout_response = client.post(reverse("logout"))

        self.assertEqual(registration_response.status_code, 403)
        self.assertEqual(login_response.status_code, 403)
        self.assertEqual(logout_response.status_code, 403)
        self.assertFalse(Customer.objects.exists())


class ReservationViewTests(TestCase):
    def create_sample_slot(self):
        return TimeSlot.objects.create(start_time=time(18, 0))

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
        self.assertContains(response, 'hx-post="/reservations/availability/"')
        self.assertContains(response, 'id="availability-result"')

    def test_authenticated_reservation_uses_existing_customer(self):
        customer = Customer.objects.create(
            name="Alice",
            login="alice",
            password=make_password("secret-password"),
        )
        Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()
        session = self.client.session
        session["authorized_customer_login"] = customer.login
        session.save()

        form_response = self.client.get(reverse("reservation-form"))
        reservation_response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Mallory",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )

        reservation = Reservation.objects.get()
        self.assertContains(form_response, 'value="Alice"')
        self.assertContains(form_response, "readonly")
        self.assertRedirects(
            reservation_response,
            reverse("reservation-detail", args=[reservation.id]),
        )
        self.assertEqual(reservation.customer, customer)
        self.assertEqual(Customer.objects.count(), 1)

    def test_my_reservations_shows_only_authenticated_customer_reservations(self):
        customer = Customer.objects.create(name="Alice", login="alice", password="hash")
        other_customer = Customer.objects.create(
            name="Bob", login="bob", password="hash"
        )
        table = Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()
        reservation = Reservation.objects.create(
            customer=customer,
            reservation_date=date(2026, 8, 1),
            time_slot=slot,
            guest_count=2,
            table=table,
        )
        Reservation.objects.create(
            customer=other_customer,
            reservation_date=date(2026, 8, 2),
            time_slot=slot,
            guest_count=2,
            table=table,
        )
        session = self.client.session
        session["authorized_customer_login"] = customer.login
        session.save()

        response = self.client.get(reverse("my-reservations"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/my_reservations.html")
        self.assertContains(response, "2026-08-01")
        self.assertContains(
            response, reverse("reservation-detail", args=[reservation.id])
        )
        self.assertNotContains(response, "2026-08-02")

    def test_my_reservations_redirects_anonymous_visitor_to_login(self):
        response = self.client.get(reverse("my-reservations"))

        self.assertRedirects(response, reverse("login"))

    def test_reservation_availability_shows_smallest_available_table(self):
        Table.objects.create(table_number=1, capacity=4)
        suitable_table = Table.objects.create(table_number=2, capacity=2)
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-availability"),
            {
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "FancyRestaurantApp/availability_result.html")
        self.assertContains(response, "Table 2 (2 seats) is available.")
        self.assertFalse(Customer.objects.exists())
        self.assertFalse(Reservation.objects.exists())
        self.assertEqual(Table.objects.get(pk=suitable_table.pk), suitable_table)

    def test_reservation_availability_reports_when_no_table_is_suitable(self):
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-availability"),
            {
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No suitable table is available.")
        self.assertFalse(Customer.objects.exists())
        self.assertFalse(Reservation.objects.exists())

    def test_reservation_availability_returns_empty_fragment_for_invalid_input(self):
        response = self.client.post(
            reverse("reservation-availability"),
            {"guest_count": 0},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.strip(), b"")
        self.assertFalse(Customer.objects.exists())
        self.assertFalse(Reservation.objects.exists())

    def test_reservation_availability_rejects_get(self):
        response = self.client.get(reverse("reservation-availability"))

        self.assertEqual(response.status_code, 405)

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


class ReservationDateValidationTests(TestCase):
    def create_sample_slot(self):
        return TimeSlot.objects.create(start_time=time(18, 0))

    def test_restaurant_uses_tokyo_time_zone(self):
        self.assertEqual(settings.TIME_ZONE, "Asia/Tokyo")

    @patch("django.utils.timezone.localdate", return_value=date(2026, 8, 1))
    @patch(
        "django.utils.timezone.localtime",
        return_value=datetime(2026, 8, 1, 17, 59, tzinfo=timezone.utc),
    )
    def test_reservation_form_rejects_past_date_and_accepts_today_and_future_date(
        self, _mocked_localtime, _mocked_localdate
    ):
        Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()

        past_response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-07-31",
                "time_slot": slot.id,
            },
        )
        today_response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-01",
                "time_slot": slot.id,
            },
        )
        future_response = self.client.post(
            reverse("reservation-form"),
            {
                "customer_name": "Alice",
                "guest_count": 2,
                "reservation_date": "2026-08-02",
                "time_slot": slot.id,
            },
        )

        self.assertEqual(past_response.status_code, 200)
        self.assertContains(past_response, "Reservation date cannot be in the past.")
        self.assertRedirects(today_response, reverse("reservation-detail", args=[1]))
        self.assertRedirects(future_response, reverse("reservation-detail", args=[2]))
        self.assertEqual(Reservation.objects.count(), 2)

    @patch("django.utils.timezone.localdate", return_value=date(2026, 8, 1))
    def test_reservation_availability_rejects_past_date(self, _mocked_localdate):
        Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()

        response = self.client.post(
            reverse("reservation-availability"),
            {
                "guest_count": 2,
                "reservation_date": "2026-07-31",
                "time_slot": slot.id,
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.strip(), b"")

    def test_reservation_form_rejects_elapsed_time_slot_today(self):
        Table.objects.create(table_number=1, capacity=2)
        before_slot = TimeSlot.objects.create(start_time=time(17, 59))
        current_slot = TimeSlot.objects.create(start_time=time(18, 0))
        future_slot = TimeSlot.objects.create(start_time=time(18, 1))

        with (
            patch("django.utils.timezone.localdate", return_value=date(2026, 8, 1)),
            patch(
                "django.utils.timezone.localtime",
                return_value=datetime(2026, 8, 1, 18, 0, tzinfo=timezone.utc),
            ),
        ):
            before_response = self.client.post(
                reverse("reservation-form"),
                {
                    "customer_name": "Alice",
                    "guest_count": 2,
                    "reservation_date": "2026-08-01",
                    "time_slot": before_slot.id,
                },
            )
            current_response = self.client.post(
                reverse("reservation-form"),
                {
                    "customer_name": "Alice",
                    "guest_count": 2,
                    "reservation_date": "2026-08-01",
                    "time_slot": current_slot.id,
                },
            )
            future_response = self.client.post(
                reverse("reservation-form"),
                {
                    "customer_name": "Alice",
                    "guest_count": 2,
                    "reservation_date": "2026-08-01",
                    "time_slot": future_slot.id,
                },
            )
            tomorrow_response = self.client.post(
                reverse("reservation-form"),
                {
                    "customer_name": "Alice",
                    "guest_count": 2,
                    "reservation_date": "2026-08-02",
                    "time_slot": current_slot.id,
                },
            )

        self.assertContains(before_response, "Reservation time must be in the future.")
        self.assertContains(current_response, "Reservation time must be in the future.")
        self.assertRedirects(future_response, reverse("reservation-detail", args=[1]))
        self.assertRedirects(tomorrow_response, reverse("reservation-detail", args=[2]))

    def test_reservation_availability_rejects_elapsed_time_slot_today(self):
        Table.objects.create(table_number=1, capacity=2)
        slot = self.create_sample_slot()

        with (
            patch("django.utils.timezone.localdate", return_value=date(2026, 8, 1)),
            patch(
                "django.utils.timezone.localtime",
                return_value=datetime(2026, 8, 1, 18, 0, tzinfo=timezone.utc),
            ),
        ):
            response = self.client.post(
                reverse("reservation-availability"),
                {
                    "guest_count": 2,
                    "reservation_date": "2026-08-01",
                    "time_slot": slot.id,
                },
                HTTP_HX_REQUEST="true",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.strip(), b"")

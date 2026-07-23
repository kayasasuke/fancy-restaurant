from datetime import date, time

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

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

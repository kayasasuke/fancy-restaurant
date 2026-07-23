from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["capacity", "table_number"]
        indexes = [
            models.Index(fields=["capacity", "table_number"]),
            models.Index(fields=["is_active", "capacity"]),
        ]

    def __str__(self) -> str:
        return f"Table {self.table_number} ({self.capacity} seats)"


class TimeSlot(models.Model):
    start_time = models.TimeField(unique=True)
    duration_minutes = models.PositiveIntegerField(
        default=90,
        validators=[MinValueValidator(1)],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["is_active", "start_time"]),
        ]

    def __str__(self) -> str:
        return self.start_time.strftime("%H:%M")


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reservations",
    )
    customer_name = models.CharField(max_length=100)
    reservation_date = models.DateField(db_index=True)
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    guest_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["reservation_date", "time_slot__start_time", "table__table_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["reservation_date", "time_slot", "table"],
                name="unique_reservation_table_slot",
            )
        ]
        indexes = [
            models.Index(fields=["reservation_date", "status"]),
            models.Index(fields=["customer_name"]),
        ]

    def __str__(self) -> str:
        return (
            f"{self.customer_name} on {self.reservation_date} "
            f"at {self.time_slot} - {self.table}"
        )

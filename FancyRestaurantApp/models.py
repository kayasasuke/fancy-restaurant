from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["login"],
                condition=~models.Q(login=""),
                name="unique_nonempty_customer_login",
            )
        ]

    def __str__(self) -> str:
        return self.name


class Table(models.Model):
    table_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Table {self.table_number} ({self.capacity} seats)"


class TimeSlot(models.Model):
    start_time = models.TimeField()

    def __str__(self) -> str:
        return self.start_time.strftime("%H:%M")


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    guest_count = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.customer.name} -> {self.table} ({self.reservation_date})"

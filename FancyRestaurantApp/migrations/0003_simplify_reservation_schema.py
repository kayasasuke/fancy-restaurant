from django.db import migrations, models
import django.db.models.deletion


def create_customers_for_existing_reservations(apps, schema_editor):
    Customer = apps.get_model("reservations", "Customer")
    Reservation = apps.get_model("reservations", "Reservation")

    for reservation in Reservation.objects.all():
        customer = Customer.objects.create(
            name=reservation.customer_name[:20],
            login="",
            password="",
        )
        reservation.customer = customer
        reservation.save(update_fields=["customer"])


class Migration(migrations.Migration):

    dependencies = [
        (
            "reservations",
            "0002_remove_reservation_unique_reservation_table_slot_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("login", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="reservation",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reservations.customer",
            ),
        ),
        migrations.RunPython(create_customers_for_existing_reservations),
        migrations.RemoveConstraint(
            model_name="reservation",
            name="unique_reservation_table_slot",
        ),
        migrations.RemoveIndex(
            model_name="reservation",
            name="reservation_reserva_4f8570_idx",
        ),
        migrations.RemoveIndex(
            model_name="reservation",
            name="reservation_custome_1e343c_idx",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="customer_name",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="status",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="user",
        ),
        migrations.AlterField(
            model_name="reservation",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="reservations.customer",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="guest_count",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="reservation_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="table",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="reservations.table",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="time_slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="reservations.timeslot",
            ),
        ),
        migrations.AlterModelOptions(
            name="reservation",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="table",
            name="reservation_capacit_2f796b_idx",
        ),
        migrations.RemoveIndex(
            model_name="table",
            name="reservation_is_acti_4c9741_idx",
        ),
        migrations.RemoveField(
            model_name="table",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="table",
            name="capacity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="table",
            name="table_number",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterModelOptions(
            name="table",
            options={},
        ),
        migrations.RemoveField(
            model_name="timeslot",
            name="duration_minutes",
        ),
        migrations.RemoveIndex(
            model_name="timeslot",
            name="reservation_is_acti_0037e2_idx",
        ),
        migrations.RemoveField(
            model_name="timeslot",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="timeslot",
            name="start_time",
            field=models.TimeField(),
        ),
        migrations.AlterModelOptions(
            name="timeslot",
            options={},
        ),
    ]

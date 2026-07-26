from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone


def validate_reservation_date(reservation_date):
    if reservation_date < timezone.localdate():
        raise forms.ValidationError("Reservation date cannot be in the past.")
    return reservation_date


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    login = forms.CharField(label="Login", max_length=20)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )
    password_confirmation = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(),
    )

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get("password")
            and cleaned_data.get("password_confirmation")
            and cleaned_data["password"] != cleaned_data["password_confirmation"]
        ):
            self.add_error("password_confirmation", "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=20)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )


class ReservationForm(forms.Form):
    customer_name = forms.CharField(label="Name", max_length=20)
    guest_count = forms.IntegerField(label="Guests", min_value=1)
    reservation_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    time_slot = forms.ChoiceField(label="Time slot")

    def __init__(self, *args, time_slots, customer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reservation_date"].widget.attrs[
            "min"
        ] = timezone.localdate().isoformat()
        self.fields["time_slot"].choices = [
            (str(slot.pk), str(slot)) for slot in time_slots
        ]
        for field_name in ("guest_count", "reservation_date", "time_slot"):
            self.fields[field_name].widget.attrs.update(
                {
                    "hx-post": "/reservations/availability/",
                    "hx-target": "#availability-result",
                    "hx-include": "closest form",
                }
            )
        if customer is not None:
            self.fields["customer_name"].initial = customer.name
            self.fields["customer_name"].widget.attrs["readonly"] = True

    def clean_reservation_date(self):
        return validate_reservation_date(self.cleaned_data["reservation_date"])


class AvailabilityForm(forms.Form):
    guest_count = forms.IntegerField(min_value=1)
    reservation_date = forms.DateField()
    time_slot = forms.ChoiceField()

    def __init__(self, *args, time_slots, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time_slot"].choices = [
            (str(slot.pk), str(slot)) for slot in time_slots
        ]

    def clean_reservation_date(self):
        return validate_reservation_date(self.cleaned_data["reservation_date"])

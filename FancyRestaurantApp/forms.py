from django import forms


class ReservationForm(forms.Form):
    customer_name = forms.CharField(label="Name", max_length=20)
    guest_count = forms.IntegerField(label="Guests", min_value=1)
    reservation_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    time_slot = forms.ChoiceField(label="Time slot")

    def __init__(self, *args, time_slots, **kwargs):
        super().__init__(*args, **kwargs)
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


class AvailabilityForm(forms.Form):
    guest_count = forms.IntegerField(min_value=1)
    reservation_date = forms.DateField()
    time_slot = forms.ChoiceField()

    def __init__(self, *args, time_slots, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time_slot"].choices = [
            (str(slot.pk), str(slot)) for slot in time_slots
        ]

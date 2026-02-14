import datetime
from django import forms
from django.utils import timezone
from datetime import time
from .models import Reservation
from django.contrib.auth.models import User


TIME_CHOICES = [
    (time(17, 0), "17:00"),
    (time(17, 30), "17:30"),
    (time(18, 0), "18:00"),
    (time(18, 30), "18:30"),
    (time(19, 0), "19:00"),
    (time(19, 30), "19:30"),
    (time(20, 0), "20:00"),
    (time(20, 30), "20:30"),
    (time(21, 0), "21:00"),
    (time(21, 30), "21:30"),
]


# Form for user to book a table
class ReservationForm(forms.ModelForm):

    time = forms.TypedChoiceField(
        choices=[],
        coerce=lambda x: datetime.datetime.strptime(x, "%H:%M:%S").time(),
        label="Time"
    )

    class Meta:
        model = Reservation
        fields = ["name", "email", "table", "date", "time", "guests"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Method for Dynamic Time Filtering
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        selected_date = None

        date_str = self.data.get("date")

        if date_str:
            try:
                selected_date = forms.DateField().to_python(date_str)
            except forms.ValidationError:
                selected_date = None

        filtered_times = []

        for t, label in TIME_CHOICES:
            if selected_date == today:
                if t > current_time:
                    filtered_times.append((t, label))
            else:
                filtered_times.append((t, label))

        self.fields["time"].choices = filtered_times

    # Data validation for date and time
    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get("date")
        time_value = cleaned_data.get("time")

        today = timezone.localdate()
        now_time = timezone.localtime().time()

        if date and date < today:
            raise forms.ValidationError(
                "You cannot book a reservation in the past."
            )

        if date == today and time_value and time_value < now_time:
            raise forms.ValidationError(
                "You cannot book a time that has already passed today."
            )

        return cleaned_data


# Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Confirm password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise forms.ValidationError(
                "Passwords do not match"
            )
        return cd.get("password2")

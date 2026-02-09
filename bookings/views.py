from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import ReservationForm


def book_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.clean()
                reservation.save()
                return redirect('reservation_success')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ReservationForm()

    return render(request, 'bookings/book_table.html', {'form': form})


def reservation_success(request):
    return render(request, 'bookings/reservation_success.html')

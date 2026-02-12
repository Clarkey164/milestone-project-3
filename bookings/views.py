from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .forms import ReservationForm
from .models import Reservation


# CREATE
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


# READ - View ALL Reservations
def reservation_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'bookings/reservation_list.html',
                  {'reservations': reservations})


# READ - Individual Reservation
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'bookings/reservation_detail.html',
                  {'reservation': reservation})


# UPDATE
def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'bookings/book_table.html',
                  {'form': form})


# DELETE
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')

    return render(request, 'bookings/reservation_confirm_delete.html',
                  {'reservation': reservation})

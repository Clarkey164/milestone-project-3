from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from .forms import ReservationForm, UserRegistrationForm
from .models import Reservation


# Homepage
def home(request):
    return render(request, 'bookings/home.html')


# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('reservation_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'bookings/register.html', {'form': form})


# CREATE
@login_required
def book_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.user = request.user
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
@login_required
def reservation_list(request):
    # Only shows reservations for the logged in User
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'bookings/reservation_list.html',
                  {'reservations': reservations})


# READ - Individual Reservation
@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    # Only the owner or staff can view bookings
    if reservation.user != request.user and not request.user.is_staff:
        return redirect('reservation_list')
    return render(request, 'bookings/reservation_detail.html',
                  {'reservation': reservation})


# UPDATE
@login_required
def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    # Only the owner or staff can edit
    if reservation.user != request.user and not request.user.is_staff:
        return redirect('reservation_list')

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'bookings/book_table.html', {'form': form})


# DELETE
@login_required
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    # Only the owner or staff can delete
    if reservation.user != request.user and not request.user.is_staff:
        return redirect('reservation_list')

    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')

    return render(request, 'bookings/reservation_confirm_delete.html',
                  {'reservation': reservation})

from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_table, name='bookings'),
    path('book-table/', views.book_table, name='book_table'),
    path(
        'reservation-success/',
        views.reservation_success,
        name='reservation_success'
    ),
]

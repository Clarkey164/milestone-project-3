from django.urls import path
from . import views

urlpatterns = [
    # path('', views.book_table, name='bookings'),
    path('book-table/', views.book_table, name='book_table'),
    path(
        'reservation-success/',
        views.reservation_success,
        name='reservation_success'
    ),

    # CRUD
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', views.reservation_detail,
         name='reservation_detail'),
    path('reservations/<int:pk>/edit/', views.reservation_update,
         name='reservation_update'),
    path('reservations/<int:pk>/delete/', views.reservation_delete,
         name='reservation_delete'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_table, name='book_table'),
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

    # USER LOGIN
    path('register/', views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='bookings/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

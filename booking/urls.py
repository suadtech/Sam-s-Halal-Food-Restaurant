from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('booking/create/', views.booking_create, name='booking_create'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/cancel/', views.booking_cancel, name='booking_cancel'),
    path('check-availability/', views.check_availability, name='check_availability'),
]


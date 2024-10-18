from django.urls import path
from . import views

from .views import add_cashier

from .views import reviews_view, add_review, search_flights
from .views import flight_search_view, search_flights, book_flight
from .views import search_passenger, update_passenger





urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),    
    path('cashier_home/', views.cashier_home, name='cashier_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('add_cashier/', add_cashier, name='add_cashier'),
    path('cashier_info/', views.cashier_info, name='cashier_info'),
    path('search_cashier/', views.search_cashier, name='search_cashier'),
    path('reviews/', reviews_view, name='reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('api/schedule/arrival/', views.get_arrival_schedule, name='get_arrival_schedule'),
    path('api/schedule/departure/', views.get_departure_schedule, name='get_departure_schedule'),
    path('passenger-info/', views.passenger_info, name='passenger_info'),
    path('search/', flight_search_view, name='flights'),  
    path('search_flights/', search_flights, name='search_flight'),
    path('book-flight/', book_flight, name='book_flight'),
    path('search_passenger/', search_passenger, name='search_passenger'),
    path('update_passenger/', update_passenger, name='update_passenger'),
    path('delete_passenger/', views.delete_passenger, name='delete_passenger'),



    ]
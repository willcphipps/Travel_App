from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('trips/new', views.new_trip),
    path('add_new', views.add_new),
    path('dashboard', views.dashboard),
    path('update', views.update),
    path('join/<int:trip_id>', views.join),
    path('remove/<int:trip_id>', views.remove),
    path('trips/edit/<int:trip_id>', views.edit),
    path('trips/<int:trip_id>', views.show),
]
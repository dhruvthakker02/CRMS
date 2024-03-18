from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.CarRegisterView.as_view(),name='car_register'),
    path('list/',views.CarListView.as_view(),name="car_list"),
    path('edit/<int:pk>/',views.CarEditView.as_view(),name='car_edit_form'),
    path('delete/<int:pk>/',views.CarDeleteView.as_view(),name="car_delete"),
    path('detail/<int:pk>/',views.CarDetailView.as_view(),name="car_detail"),
    path('booking/<int:pk>/',views.BookingCreateView.as_view(),name="car_booking"),
    path('booking_list/',views.BookCarListView.as_view(),name="booking_list"),
    path('booking_status_update/<int:pk>/',views.UpdateStatusView.as_view(),name="update_status"),
    path('payment/',views.Payment,name="carpayment")

]
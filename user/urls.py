from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('tenant_register/',views.TenantRegisterView.as_view(),name="tenant_register"),
    path('renter_register/',views.RenterRegisterView.as_view(),name="renter_register"),
    path('login/',views.UserLoginView.as_view(),name="login"),
    path('renter_dashboard/',views.RenterDashboardView.as_view(),name="renter_dashboard"),
    path('logout/',LogoutView.as_view(next_page='login'),name="logout"),
    path('tenant_dashboard/',views.TenantDashboardView.as_view(),name="tenant_dashboard"),
]
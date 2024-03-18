from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import TenantRegistrationForm,RenterRegistrationForm
from django.views.generic.edit import CreateView
from .models import User
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView
from car.models import Car,BookCar
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class TenantRegisterView(CreateView):
    template_name = "user/tenant_register.html"
    model = User
    form_class =  TenantRegistrationForm
    success_url= "/user/login/"

    def form_valid(self, form):
        email= form.cleaned_data.get('email')

        if sendMail(email):
            print("Mail sent successfully")
            return super().form_valid(form)
        else:
            return super().form_valid(form)

        
    

class RenterRegisterView(CreateView):
    template_name= "user/renter_register.html"
    model= User
    form_class= RenterRegistrationForm
    success_url= "/user/login/"


    def form_valid(self, form):
        email= form.cleaned_data.get('email')

        if sendMail(email):
            print("Mail sent successfully")
            return super().form_valid(form)
        else:
            return super().form_valid(form)


def sendMail(to):
    subject='Welcome to Car Rental System'
    message = 'Hope you are enjoying the user experience'
    recipientList= [to]
    EMAIL_FROM = settings.EMAIL_HOST_USER
    send_mail(subject,message,EMAIL_FROM,recipientList)
    return True

class UserLoginView(LoginView):
    template_name= 'user/login.html'
    model= User

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_renter:
                return '/user/renter_dashboard/'
            else:
                return '/user/tenant_dashboard'

# @method_decorator(login_required,name="dispatch")
# class RenterDashboardView(ListView):
#     def get(self, request, *args, **kwargs):
#         print("RenterDashboardView")
#         cars= Car.objects.filter(user=request.user)
#         print("....................",cars)

#         return render(request,'user/renter_dashboard.html',{"cars":cars})
    
#     template_name= 'user/renter_dashboard.html'
            
class RenterDashboardView(ListView):
    template_name = 'user/renter_dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Get cars owned by the current user
        cars = Car.objects.filter(user=self.request.user)

        # Get bookings associated with those cars
        bookings = BookCar.objects.filter(car__in=cars)

        return bookings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add cars of the renter to the context
        context['cars'] = Car.objects.filter(user=self.request.user)
        return context            

class TenantDashboardView(ListView):
    template_name = "user/tenant_dashboard.html"
    context_object_name = "cars"

    def get_queryset(self):
        # Fetch all cars from all renters
        return Car.objects.all()
    
    def get(self, request, *args, **kwargs):
        print("TenantDashboardView")
        cars = self.get_queryset()
        print("................", cars)
        return render(request, self.template_name, {"cars": cars})

        





from typing import Any
from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Car
from .forms import CarCreationForm, BookingCreationForm
from user.models import User
from django.views.generic import ListView,DetailView
from car.models import Car,BookCar
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#method decorator login required.....
@method_decorator(login_required,name="dispatch")
class CarRegisterView(CreateView):
    template_name= 'car/register.html'
    model= Car
    form_class= CarCreationForm
    success_url= '/car/list/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if form.is_bound and 'user' in form.fields:
            # Customize the queryset for the user field based on is_renter condition
            form.fields['user'].queryset = User.objects.filter(is_renter=True)
        return form
    
    def form_valid(self, form):
        print("method called....")
        form.instance.user = self.request.user
        return super().form_valid(form)
    
@method_decorator(login_required,name="dispatch")    
class CarListView(ListView):
    def get(self, request, *args, **kwargs):
        cars = Car.objects.filter(user=request.user)
        return render(request,'car/list.html',{"cars":cars})
    
    template_name= 'car/list.html'

    

class CarEditView(UpdateView):
    model= Car
    form_class= CarCreationForm
    success_url= '/car/list/'
    template_name= 'car/edit_form.html'    

class CarDeleteView(DeleteView):
    model= Car
    template_name= 'car/delete.html'

    success_url= '/car/list/'
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        # Get the car object
        car = self.get_object()

        # Manually delete related Booking records
        bookings_to_delete = car.bookcar_set.all()
        for booking in bookings_to_delete:
            booking.delete()

        # Delete the car
        return super().delete(request, *args, **kwargs)

class CarDetailView(DetailView):
    model= Car
    context_object_name= 'car'
    template_name= 'car/detail.html'



class BookingCreateView(CreateView):
    model = BookCar
    template_name = 'car/booking.html'
    form_class = BookingCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the car object from the CarDetailView
        car = get_object_or_404(Car, pk=self.kwargs['pk'])

        # Add the car object to the context
        context['car'] = car
        return context

    def form_valid(self, form):
        # You can access the car object from the context
        car = self.get_context_data().get('car')

        # Do something with the car object, for example, save it to the Booking object
        form.instance.car = car
        return super().form_valid(form)

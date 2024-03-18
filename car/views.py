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
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string




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




class BookingCreateView(LoginRequiredMixin, CreateView):
    model = BookCar
    template_name = 'car/booking.html'
    form_class = BookingCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the car object from the CarDetailView
        car = get_object_or_404(Car, pk=self.kwargs['pk'])
        print("car....",car)
        renter = car.user
        print("renter,,,,,",renter)

        # Get the logged-in user
        logged_in_user = self.request.user
        print("loggedin user",logged_in_user)
        # Add the car and logged-in user objects to the context
        context['car'] = car
        #context['logged_in_user'] = logged_in_user
        context['renter'] = renter
        return context

    def form_valid(self, form):
        # You can access the car object from the context
        car = self.get_context_data().get('car')
        print("car1",car)

        print("Car:", car)
        #print("Logged-in user:", logged_in_user)
        print("Renter associated with the car:", car.user)
        # Get the logged-in user
        #logged_in_user = self.request.user
        start_hour = form.cleaned_data.get('start_hour')
        print("start hour",start_hour)

        end_hour = form.cleaned_data.get('end_hour')
        car_base_price = car.cost_per_hour

        duration_hours = (end_hour - start_hour).total_seconds() / 3600  # Convert timedelta to hours


        total_price = duration_hours * car_base_price
        print("total price",total_price)
        # Set the calculated total price in the form before saving
        form.instance.total_price = total_price
        # Assign the car and renter (logged-in user) to the booking
        form.instance.car = car
        form.instance.renter =car.user
        form.instance.tenant = self.request.user
        form.instance.status = "Pending"

        return super().form_valid(form)



class BookCarListView(ListView):
    model = BookCar
    template_name = 'car/booking_list.html'  # Provide the template name where you want to display the list
    context_object_name = 'bookings'

    def get_queryset(self):
        # Get the logged-in user (assuming you are using Django's built-in authentication)
        user = self.request.user

        # Filter bookings where the renter is the logged-in user
        queryset = BookCar.objects.filter(renter=user)

        return queryset



# class UpdateStatusView(View):
    
#     def post(self, request, pk):
#         booking = BookCar.objects.get(id=pk)
        
#         # Retrieve the hidden action value from the form
#         action = request.POST.get('action')

#         # Perform different actions based on the hidden value
#         if action == 'approve':
#             booking.status = "Booked"
#             subject = 'Booking Approved'
#             message = 'Your car booking has been approved and is now confirmed.'
#         elif action == 'reject':
#             booking.status = "Rejected"
#             subject = 'Booking Rejected'
#             message = 'Sorry, we couldn\'t book your car as it is not available for the desired timings.'

#         # Save the changes and redirect
#         booking.save()

#         EMAIL_FROM = settings.EMAIL_HOST_USER
#         # Send email to the tenant
#         send_mail(subject, message,EMAIL_FROM, [booking.tenant_email])

#         return redirect(reverse('booking_list'))


class UpdateStatusView(View):
   
    def post(self, request, pk):
        booking = BookCar.objects.get(id=pk)
        
        # Retrieve the hidden action value from the form
        action = request.POST.get('action')

        # Perform different actions based on the hidden value
        if action == 'approve':
            booking.status = "Booked"
            # Send email to tenant
            self.send_approval_email(booking)
        elif action == 'reject':
            booking.status = "Rejected"
            # Send email to tenant
            self.send_rejection_email(booking)

        # Save the changes and redirect
        booking.save()
        messages.success(request, "Booking status updated successfully.")
        return redirect(reverse('booking_list'))

    def send_approval_email(self, booking):
        
        subject = 'Car Booking Approval'
        context = {'booking': booking}
        context['car'] = booking.car  # Add the car object to the context
        message = render_to_string('car/booking_approval_email.html', context)
        from_email = settings.EMAIL_HOST_USER
        to_email = booking.tenant.email
        send_mail(subject, message, from_email, [to_email], html_message=message)

    def send_rejection_email(self, booking):
        subject = 'Car Booking Rejection'
        message = render_to_string('car/booking_rejection_email.html', {'booking': booking})
        from_email = settings.EMAIL_HOST_USER
        to_email = booking.tenant.email
        send_mail(subject, message, from_email, [to_email], html_message=message)

def Payment(request):
    return render(request,"car/payment.html")    

        


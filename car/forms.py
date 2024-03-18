from django import forms
from .models import Car,BookCar
 

class CarCreationForm(forms.ModelForm):
    class Meta:
        model= Car
        #fields= "__all__"
        exclude=["user"]

class BookingCreationForm(forms.ModelForm):
    total_price = forms.FloatField(initial=0, widget=forms.HiddenInput())

    class Meta:
        model= BookCar
        #fields= "__all__"
        exclude = ["renter","tenant","car","status"]
        widgets = {
            'start_hour': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_hour': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



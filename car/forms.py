from django import forms
from .models import Car,BookCar
 

class CarCreationForm(forms.ModelForm):
    class Meta:
        model= Car
        #fields= "__all__"
        exclude=["user"]

class BookingCreationForm(forms.ModelForm):
    class Meta:
        model= BookCar
        fields= "__all__"
    



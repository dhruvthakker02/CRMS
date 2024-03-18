from django.db import models
from user.models import User

# Create your models here.

CarType= (
    ('Hatchback','Hatchback'),
    ('Sedan','Sedan'),
    ('SUV','SUV'),
)

CarFuelType= (
    ('Diesel','Diesel'),
    ('Petrol','Petrol'),
    ('CNG','CNG'),
    ('EV','EV')
)

class Car(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    model= models.CharField(max_length=100)
    type= models.CharField(max_length=100,choices=CarType)
    color= models.CharField(max_length=100)
    fuel_type= models.CharField(max_length=100,choices=CarFuelType)
    seating_capacity= models.IntegerField()
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    cost_per_hour= models.IntegerField()

    class Meta():
        db_table= "car"

    def __str__(self):
        return self.model    


BookStatus =(
    ('Booked','Booked'),
    ('Pending','Pending'),
    ('Rejected','Rejected')
)

class BookCar(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter_bookings')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    start_hour = models.DateTimeField()
    end_hour = models.DateTimeField()
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    is_outercity = models.BooleanField()
    total_price = models.IntegerField()
    status = models.CharField(max_length=100, choices=BookStatus)

    class Meta:
        db_table='booking'

    def __str__(self):
        return self.car.model   







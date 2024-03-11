from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    id_proof = models.ImageField(upload_to="id_proofs/", null=True, blank=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    is_renter = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

    class Meta:
        db_table="user"
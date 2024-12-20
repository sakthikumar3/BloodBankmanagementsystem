from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=10, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    contact = models.CharField(max_length=15)
    units_donated = models.PositiveIntegerField()
    donated_date = models.DateTimeField(auto_now_add=True)

class BloodStock(models.Model):
    blood_group = models.CharField(max_length=10, unique=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    units_available = models.PositiveIntegerField(default=0)
    
@receiver(post_save, sender=Donor)
def update_blood_stock(sender, instance, **kwargs):
    try:
        # Check if the blood group exists in BloodStock
        stock, created = BloodStock.objects.get_or_create(blood_group=instance.blood_group)
        # Add the donated units to the stock
        stock.units_available += instance.units_donated
        stock.save()
    except Exception as e:
        print(f"Error updating blood stock: {e}")


class BloodRequest(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    units_requested = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ], default='Pending')

class DonationCamp(models.Model):
    camp_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    contact = models.CharField(max_length=15)

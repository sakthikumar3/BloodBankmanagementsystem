from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donor, BloodStock

@receiver(post_save, sender=Donor)
def update_blood_stock(sender, instance, **kwargs):
    try:
        # Get or create the BloodStock entry for the given blood group
        blood_stock, created = BloodStock.objects.get_or_create(blood_group=instance.blood_group)
        # Update the units_available field with the donated units
        blood_stock.units_available += instance.units_donated
        blood_stock.save()
    except Exception as e:
        print(f"Error updating blood stock: {e}")

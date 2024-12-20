from django import forms
from .models import Donor, BloodRequest, DonationCamp
from .models import DonationCamp

class AddCampForm(forms.ModelForm):
    class Meta:
        model = DonationCamp
        fields = ['camp_name', 'location', 'start_date', 'end_date', 'contact']
        
# Donor Form
class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'age', 'blood_group', 'contact', 'units_donated']
        widgets = {
            'donated_date': forms.HiddenInput(),
        }

# BloodRequest Form
class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['name', 'blood_group', 'units_requested', 'contact']
        widgets = {
            'request_date': forms.HiddenInput(),
        }

# DonationCamp Form
class DonationCampForm(forms.ModelForm):
    class Meta:
        model = DonationCamp
        fields = ['camp_name', 'location', 'start_date', 'end_date', 'contact']

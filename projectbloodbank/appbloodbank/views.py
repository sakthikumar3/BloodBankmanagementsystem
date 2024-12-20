from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor, BloodStock, BloodRequest, DonationCamp
from .forms import DonorForm, BloodRequestForm, DonationCampForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Donor, BloodStock, BloodRequest, DonationCamp
import datetime
from .forms import AddCampForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

def home(request):
    blood_requests = BloodRequest.objects.all()  # Replace with your queryset
    return render(request, 'home.html', {'blood_requests': blood_requests})

def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the admin dashboard
            return redirect(reverse('admin_dashboard'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Donor View
def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save()  # Save the donor data
            # Update the blood stock for the blood group
            blood_group = donor.blood_group
            units_donated = donor.units_donated
            stock, created = BloodStock.objects.get_or_create(blood_group=blood_group)
            stock.units_available += units_donated
            stock.save()
            return redirect('donor_success')
    else:
        form = DonorForm()
    return render(request, 'register_donor.html', {'form': form})

def donor_success(request):
    return render(request, 'donor_success.html') 

# BloodRequest View
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()  # Save the blood request
            return redirect('request_success')
    else:
        form = BloodRequestForm()
    return render(request, 'request_blood.html', {'form': form})

# DonationCamp View
def create_donation_camp(request):
    if request.method == 'POST':
        form = DonationCampForm(request.POST)
        if form.is_valid():
            form.save()  # Save the donation camp details
            return redirect('camp_success')
    else:
        form = DonationCampForm()
    return render(request, 'create_donation_camp.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Admin Dashboard
def admin_dashboard(request):
    donor_count = Donor.objects.count()
    total_units = sum(stock.units_available for stock in BloodStock.objects.all())
    pending_requests = BloodRequest.objects.filter(status='Pending').count()
    upcoming_camps = DonationCamp.objects.filter(start_date__gte=datetime.date.today()).count()

    context = {
        'donor_count': donor_count,
        'total_units': total_units,
        'pending_requests': pending_requests,
        'upcoming_camps': upcoming_camps,
    }
    return render(request, 'admin_dashboard.html', context)

# Donor List
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor_list.html', {'donors': donors})

# Blood Stock
def blood_stock_view(request):
    blood_stock = BloodStock.objects.all()
    total_units = sum(stock.units_available for stock in blood_stock)
    return render(request, 'blood_stock.html', {
        'blood_stock': blood_stock,
        'total_units': total_units,
    })


# Blood Requests
def blood_requests(request):
    requests = BloodRequest.objects.all()
    return render(request, 'blood_requests.html', {'requests': requests})

# Handle Accept/Reject for Blood Requests
def update_blood_request_status(request, pk, status):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    blood_request.status = status
    blood_request.save()
    return redirect('blood-requests')

from django.shortcuts import render, get_object_or_404
from .models import BloodRequest  # Ensure the correct model is imported 

def receiver_status(request):

    blood_requests = BloodRequest.objects.all()
    for blood_request in blood_requests:
        if blood_request.status == "Accepted":
            blood_request.message = f"Your request is accepted for {blood_request.name}."
        elif blood_request.status == "Rejected":
            blood_request.message = "Sorry to say this, your blood request is not stock so reject the request ."
        else:
            blood_request.message = "Your blood request is still pending."

    return render(request, "receiver_status.html", {'blood_requests': blood_requests})


def accept_request(request, request_id):
    return redirect('receiver_status', request_id=request_id)

def donation_camps(request):
    camps = DonationCamp.objects.all()
    return render(request, 'donation_camps.html', {'camps': camps})


def add_camp_view(request):
    if request.method == 'POST':
        form = AddCampForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AddCampForm()
    return render(request, 'add_camp.html', {'form': form})

def request_success(request):
    return render(request,'request_success.html')

def camp_list(request):
    camps = DonationCamp.objects.all()  
    return render(request, 'camp.html', {'camps': camps})

# Edit Donor
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor-list')  # Redirect to the donor list
    else:
        form = DonorForm(instance=donor)
    return render(request, 'edit_donor.html', {'form': form})

# Delete Donor
def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        return redirect('donor-list')  # Redirect to the donor list
    return render(request, 'confirm_delete_donor.html', {'donor': donor})

def edit_donation_camp(request, id):
    camp = get_object_or_404(DonationCamp, id=id)

    if request.method == 'POST':
        form = DonationCampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('donation-camps')  # Redirect to the list of donation camps
    else:
        form = DonationCampForm(instance=camp)

    return render(request, 'edit_donation_camp.html', {'form': form})

def delete_donation_camp(request, id):
    camp = get_object_or_404(DonationCamp, id=id)
    camp.delete()
    return redirect('donation-camps')

def create_or_edit_donation_camp(request, id=None):
    if id:  # If an ID is provided, it's editing an existing camp 
        camp = get_object_or_404(DonationCamp, id=id)
    else:  # If no ID, it's a new camp
        camp = None

    if request.method == 'POST':
        form = DonationCampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('donation-camps')  # Redirect after saving
    else:
        form = DonationCampForm(instance=camp)

    return render(request, 'create_edit_camp.html', {'form': form})


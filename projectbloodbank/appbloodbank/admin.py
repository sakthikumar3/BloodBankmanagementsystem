from django.contrib import admin
from .models import Donor, BloodStock,BloodRequest

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'units_donated', 'donated_date')

@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units_available')

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'units_requested', 'contact', 'request_date', 'status')
    list_filter = ('blood_group', 'status')
    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        queryset.update(status='Accepted')
        self.message_user(request, "Selected requests have been accepted.")
    accept_requests.short_description = "Accept Selected Requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected requests have been rejected.")
    reject_requests.short_description = "Reject Selected Requests"


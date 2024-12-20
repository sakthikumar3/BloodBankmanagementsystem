from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login_views',views.login_views,name='login'),
    path('register-donor/', views.register_donor, name='register_donor'),
    path('donor_sucess',views.donor_success,name='donor_success'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/donor-list/', views.donor_list, name='donor-list'),
    path('donor_list/edit/<int:pk>/', views.edit_donor, name='edit-donor'),
    path('donor_list/delete/<int:pk>/', views.delete_donor, name='delete-donor'),
    path('admin/blood-stock/', views.blood_stock_view, name='blood_stock'),
    path('admin/blood-requests/', views.blood_requests, name='blood-requests'),
    path('receiver-status/', views.receiver_status, name='receiver_status'),
    path('admin/blood-requests/<int:pk>/<str:status>/', views.update_blood_request_status, name='update-blood-request-status'),
    path('admin/donation-camps/', views.donation_camps, name='donation-camps'),
    path('delete-donation-camp/<int:id>/', views.delete_donation_camp, name='delete-donation-camp'),
    path('create-donation-camp/', views.create_or_edit_donation_camp, name='create-donation-camp'),
    path('edit-donation-camp/<int:id>/', views.create_or_edit_donation_camp, name='edit-donation-camp'),
    path('edit-donation-camp/<int:id>/', views.edit_donation_camp, name='edit-donation-camp'),
    path('add-camp/', views.add_camp_view, name='add_camp'),
    path('request_success/',views.request_success,name='request_success'),
    path('camps/', views.camp_list, name='camp_list'),
]

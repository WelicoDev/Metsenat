from django.contrib import admin
from .models import Sponsor, Student, AllocatedAmount

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'payment_type', 'amount', 'status', 'payment_method', 'company_name', 'created_at', 'updated_at']
    search_fields = ['full_name', 'phone_number']
    list_filter = ['status', 'payment_type', 'payment_method']
    ordering = ['-created_at']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'university', 'degree_type', 'contract_amount', 'created_at', 'updated_at']
    search_fields = ['full_name', 'phone_number']
    list_filter = ['degree_type', 'university']
    ordering = ['-created_at']

@admin.register(AllocatedAmount)
class AllocatedAmountAdmin(admin.ModelAdmin):
    list_display = ['id', 'sponsor_id', 'student_id', 'money', 'created_at', 'updated_at']
    search_fields = ['sponsor_id__full_name', 'student_id__full_name']
    list_filter = ['sponsor_id', 'student_id']
    ordering = ['-created_at']


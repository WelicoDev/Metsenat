from django.contrib import admin
from .models import Sponsor, Student, University, AllocatedAmount

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'amount', 'status', 'payment_method', 'payment_type', 'company_name')
    list_filter = ('status', 'payment_method', 'payment_type')
    search_fields = ('full_name', 'phone_number', 'company_name')
    ordering = ('-created_at',)
    list_editable = ('status',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'degree_type', 'university', 'contract_amount')
    list_filter = ('degree_type', 'university')
    search_fields = ('full_name', 'phone_number')

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AllocatedAmount)
class AllocatedAmountAdmin(admin.ModelAdmin):
    list_display = ('sponsor_id', 'student_id', 'money')
    list_filter = ('sponsor_id', 'student_id')
    search_fields = ('sponsor_id__full_name', 'student_id__full_name')

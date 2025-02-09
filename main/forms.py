from django import forms
from .models import Sponsor, Student, AllocatedAmount

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['payment_type', 'full_name', 'phone_number', 'status', 'amount', 'payment_method', 'company_name', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        payment_type = cleaned_data.get('payment_type')
        company_name = cleaned_data.get('company_name')

        # Yuridik shaxs bo‘lsa, kompaniya nomi kiritilishi shart
        if payment_type == Sponsor.LEGAL_ENTITY and not company_name:
            self.add_error('company_name', 'Kompaniya nomi kiritilishi shart!')

        return cleaned_data

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'phone_number', 'degree_type', 'university', 'contract_amount']

class AllocatedAmountForm(forms.ModelForm):
    class Meta:
        model = AllocatedAmount
        fields = ['sponsor_id', 'student_id', 'money']

    def clean_money(self):
        money = self.cleaned_data.get('money')
        if money <= 0:
            raise forms.ValidationError("Ajratilgan summa 0 dan katta bo‘lishi kerak!")
        return money

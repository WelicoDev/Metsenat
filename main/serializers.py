# from rest_framework import serializers
# from .models import Sponsor
#
# class SponsorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sponsor
#         fields = '__all__'
#
#     def validate(self, data):
#         if data.get('payment_type') == Sponsor.INDIVIDUAL:
#             data['company_name'] = None
#
#         if data.get('payment_type') == Sponsor.LEGAL_ENTITY and not data.get('company_name'):
#             raise serializers.ValidationError({"company_name": "Yuridik shaxs uchun kompaniya nomi kiritish majburiy!"})
#
#         if self.context.get("request").data.get("custom_amount", False):
#             data['amount'] = 0
#
#         return data
from rest_framework import serializers
from .models import Sponsor, University, Student, AllocatedAmount

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

    def validate(self, data):
        if data.get('payment_type') == Sponsor.INDIVIDUAL:
            data['company_name'] = None  # Jismoniy shaxs uchun tashkilot nomi bo'sh bo'ladi
        return data


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class AllocatedAmountSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = AllocatedAmount
        fields = '__all__'

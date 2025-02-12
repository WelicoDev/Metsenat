from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import Sponsor, Student, AllocatedAmount, University, LEGAL_ENTITY, INDIVIDUAL
from django.db.models import Sum


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    money_spent = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = [
            'id',
            'full_name',
            'phone_number',
            'amount',
            'money_spent',
            'status',
            'company_name',
            'payment_method',
            'payment_type',
            'comment'
        ]

    def get_money_spent(self, obj):
        result = AllocatedAmount.objects.filter(sponsor_id=obj).aggregate(total=Sum('money'))
        return result['total'] or 0

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)  # when updating a sponsor, it attaches instance to it.
        company_name = attrs.get('company_name')
        payment_type = attrs.get('payment_type')

        if payment_type == LEGAL_ENTITY and not company_name:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Company name is required for legal entities.'
                }
            )

        if instance and instance.payment_type == LEGAL_ENTITY and payment_type == INDIVIDUAL:
            attrs['company_name'] = None  # Clear company name field when changing from legal entity to individual

        if payment_type == INDIVIDUAL and company_name:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Individuals should not have company name.'
                }
            )

        return attrs


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    covered_contract_amount = serializers.SerializerMethodField()
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone_number', 'degree_type', 'university', 'contract_amount', 'covered_contract_amount']

    def get_covered_contract_amount(self, obj):
        result = AllocatedAmount.objects.filter(student_id=obj).aggregate(total=Sum('money'))
        return result['total'] or 0


class AllocatedAmountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.UUIDField(write_only=True)
    student = StudentSerializer(read_only=True)
    student_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = AllocatedAmount
        fields = ['id', 'sponsor', 'sponsor_id', 'student', 'student_id', 'money']

    def validate(self, attrs):
        sponsor_id = attrs.get('sponsor_id')
        student_id = attrs.get('student_id')

        if sponsor_id:
            if not Sponsor.objects.filter(id=sponsor_id).exists():
                raise ValidationError(
                    {
                        'success': False,
                        'message': 'Sponsor with this ID does not exist.'
                    }
                )

        if student_id:
            if not Student.objects.filter(id=student_id).exists():
                raise ValidationError(
                    {
                        'success': False,
                        'message': 'Student with this ID does not exist.'
                    }
                )

        return attrs

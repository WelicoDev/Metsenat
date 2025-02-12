from rest_framework import serializers
from .models import Sponsor, University, Student

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'phone_number', 'payment_type', 'amount', 'payment_method', 'company_name', 'status', 'comment']

    def validate(self, attrs):
        sponsor_type = attrs.get('payment_type')
        company_name = attrs.get('company_name')

        if sponsor_type == 'individual' and company_name:
            raise serializers.ValidationError('Individuals should not have a company name.')

        return attrs

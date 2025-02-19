from rest_framework import serializers
from .models import Sponsor

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'phone_number', 'payment_type', 'amount', 'payment_method', 'company_name', 'comment']

    def validate(self, attrs):
        sponsor_type = attrs.get('payment_type')
        company_name = attrs.get('company_name')


        if sponsor_type == 'individual':
            attrs['company_name'] = None

        if sponsor_type == 'legal_entity' and not company_name:
            raise serializers.ValidationError('Company name must be entered for a legal entity')

        return attrs

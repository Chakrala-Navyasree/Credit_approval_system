# serializers.py
from rest_framework import serializers
from .models import Customer, LoanResult

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'age', 'monthly_salary']

class LoanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanResult
        fields = '__all__'

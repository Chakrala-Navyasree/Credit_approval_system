# views.py
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from credit_approval_system.services import calculate_credit_score, determine_loan_eligibility
from .models import Customer, LoanData
from .serializers import CustomerSerializer

@api_view(['POST'])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    
    if serializer.is_valid():
        monthly_salary = serializer.validated_data['monthly_salary']
        serializer.validated_data['approved_limit'] = round(36 * monthly_salary, -5)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_loan_eligibility(request):
    data = request.data
    customer_id = data.get('customer_id', None)
    loan_amount = data.get('loan_amount', None)
    interest_rate = data.get('interest_rate', None)
    tenure = data.get('tenure', None)

    loan_data_instance = LoanData.objects.filter(customer_id=customer_id).first()

    if loan_data_instance:

        loan_data_instance.loan_amount = loan_amount
        loan_data_instance.interest_rate = interest_rate
        loan_data_instance.tenure = tenure

        credit_score = calculate_credit_score(loan_data_instance)

        approved_loan_amount, corrected_interest_rate = determine_loan_eligibility(
            credit_score, loan_data_instance.loan_amount, loan_data_instance.interest_rate
        )
        response_data = {
            'credit_rating': credit_score,
            'approved_loan_amount': approved_loan_amount,
            'interest_rate': corrected_interest_rate,
        }

        return JsonResponse(response_data)
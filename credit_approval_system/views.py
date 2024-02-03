# views.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from credit_approval_system.services import calculate_credit_score, determine_loan_eligibility
from .models import Customer, LoanData, LoanResult
from .serializers import CustomerSerializer, LoanResultSerializer

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
    
def view_loan_details(request, loan_id):

    loan_data_instance = get_object_or_404(LoanResult, loan_id=loan_id)
    loan_instance = get_object_or_404(LoanResult, loan_id=loan_id)
    customer_instance = get_object_or_404(Customer, customer_id=loan_data_instance.customer_id)

    response_data = {
        'loan_id': loan_data_instance.loan_id,
        'loan_amount': loan_data_instance.loan_approved,
        'tenure': loan_instance.tenure,
        'interest_rate': loan_instance.interest_rate,
        'monthly_installemts': loan_instance.monthly_repayment,
        'customer':{
        'customer_id': customer_instance.customer_id,
        'first_name': customer_instance.first_name,
        'last_name': customer_instance.last_name,
        'phone_number': customer_instance.phone_number
        }
    }

    return JsonResponse(response_data)

def view_loan_details(request, customer_id):

    loan_data_instance = get_object_or_404(LoanResult, customer_id=customer_id)
    loan_instance = get_object_or_404(LoanResult, customer_id=customer_id)
    customer_instance = get_object_or_404(Customer, customer_id=loan_data_instance.customer_id)

    response_data = {
        'loan_id': loan_data_instance.loan_id,
        'loan_amount': loan_data_instance.loan_approved,
        'tenure': loan_instance.tenure,
        'interest_rate': loan_instance.interest_rate,
        'monthly_installemts': loan_instance.monthly_repayment
    }

    return JsonResponse(response_data)

@csrf_exempt
def create_loan(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)
    customer_id = data.get('customer_id', None)
    loan_amount = float(data.get('loan_amount', 0))
    interest_rate = float(data.get('interest_rate', 0))
    tenure = int(data.get('tenure', 0))
    if customer_id is None:
        return JsonResponse({'error': 'Missing customer_id in the request body'}, status=400)

    loan_data_instance = LoanData.objects.filter(customer_id=customer_id).first()

    credit_score = calculate_credit_score(loan_data_instance)
    approved_loan_amount, corrected_interest_rate = determine_loan_eligibility(credit_score, loan_amount, interest_rate)

    if approved_loan_amount > 0:
        loan_result = LoanResult.objects.create(
            customer_id=loan_data_instance.customer_id,
            loan_id = loan_data_instance.loan_id,
            loan_approved=True,
            message='Loan approved and processed successfully',
            monthly_installment=approved_loan_amount,
        )
    else:
        loan_result = LoanResult.objects.create(
            customer_id=loan_data_instance.customer_id,
            loan_id=loan_data_instance.loan_id,
            loan_approved=False,
            message='Loan not approved based on eligibility criteria',
            monthly_installment=0,
        )
    serializer = LoanResultSerializer(loan_result)
    return Response(serializer.data)
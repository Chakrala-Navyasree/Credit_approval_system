# services.py
from django.db import models
from .models import LoanData, Customer

def calculate_credit_score(loan_data_instance):
    customer_instance = Customer.objects.get(customer_id=loan_data_instance.customer_id)
    breakpoint()
    past_loans_paid_on_time = loan_data_instance.emis_paid_on_time
    num_loans_taken_in_past = LoanData.objects.filter(customer_id=loan_data_instance.customer_id).count()
    loan_activity_in_current_year = LoanData.objects.filter(customer_id=loan_data_instance.customer_id, start_date__year=2024).count()
    loan_approved_volume = customer_instance.approved_limit

    if float(loan_data_instance.monthly_repayment) > 0.5 * float(customer_instance.monthly_salary):
        return 0  # Sum of all current EMIs > 50% of monthly salary

    if loan_data_instance.loan_amount > loan_approved_volume:
        return 0  # Sum of current loans > approved limit

    credit_score = (
        10 * past_loans_paid_on_time +
        5 * num_loans_taken_in_past +
        20 * loan_activity_in_current_year +
        30 * loan_approved_volume
    )

    return credit_score

def determine_loan_eligibility(credit_score, loan_amount, interest_rate):
    if credit_score > 50:
        approved_loan_amount = 0.8 * loan_amount
        corrected_interest_rate = interest_rate
    elif 30 < credit_score <= 50:
        approved_loan_amount = 0.9 * loan_amount
        corrected_interest_rate = max(12, interest_rate)
    elif 10 < credit_score <= 30:
        approved_loan_amount = 0.95 * loan_amount
        corrected_interest_rate = max(16, interest_rate)
    else:
        approved_loan_amount = 0
        corrected_interest_rate = 0

    return approved_loan_amount, corrected_interest_rate

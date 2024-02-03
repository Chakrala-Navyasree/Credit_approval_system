# models.py
from django.db import models

class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'customer_data'


class LoanData(models.Model):
    customer_id = models.IntegerField()
    loan_id = models.IntegerField()
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        db_table = 'loan_data'
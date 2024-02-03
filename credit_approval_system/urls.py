# urls.py (inside your app folder)
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_customer),
    path('check-eligibility/',views.check_loan_eligibility),
    path('view_loan/<int:loan_id>/', views.view_loan_details),
    path('create_loan/', views.create_loan),
]

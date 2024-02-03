# urls.py (inside your app folder)
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_customer),
]

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer
from .serializers import CustomerSerializer

@api_view(['POST'])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    
    if serializer.is_valid():
        # Calculate approved limit based on the formula
        monthly_salary = serializer.validated_data['monthly_salary']
        serializer.validated_data['approved_limit'] = round(36 * monthly_salary, -5)
        
        # Save the new customer
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

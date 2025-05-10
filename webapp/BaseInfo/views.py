from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .Serializers import UserSerializer

def index(request):
    return render(request, 'hd.html')  
def next(request):
    return render(request,'Game.html' )

@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.data if request.content_type == 'application/json' else request.POST
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if request.content_type == 'application/json':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # redirect to Myopia_Test/ after successful HTML form submission
            return redirect('base_myopia')
        if request.content_type == 'application/json':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'create_user.html', {'errors': serializer.errors})

    return render(request, 'create_user.html')
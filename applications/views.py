from django.shortcuts import render
from rest_framework import generics 
from applications.models import AppDevUser, Candidate, Trainee 
from applications.serializers import AppDevUserSerializer


# For admin view 
class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = AppDevUser.objects.all() 
	serializer_class = AppDevUserSerializer
	lookup_field = 'email'







 
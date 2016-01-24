from rest_framework import serializers
from applications.models import AppDevUser, Candidate, Trainee 

class AppDevUserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = AppDevUser
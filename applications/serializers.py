from rest_framework import serializers
from applications.models import AppDevUser, Candidate, Trainee 

# Candidate Serialzer 
class CandidateSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Candidate


# Trainee Serialier
class TraineeSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Trainee 


# AppDevUser Serializer including the above two serializers as nested serializers 
class AppDevUserSerializer(serializers.ModelSerializer):

	candidate = CandidateSerializer(many=False, read_only=True, allow_null=True)
	trainee = TraineeSerializer(many=False, read_only=True, allow_null=True)

	class Meta: 
		model = AppDevUser









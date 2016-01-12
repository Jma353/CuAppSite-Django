from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator 
from django.db import models
from django.core.exceptions import ValidationError 
import random
import string



# For the access code of Candidate and Trainee 
def generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))



# Custom essay length validator 
def validate_essay_length(essay):
	essay_array = essay.split(' ') # Split based on spaces 
	essay_array = list(filter(('').__ne__, essay_array))
	if len(essay_array) > 300: # If the essay is over 300 words 
		raise ValidationError("This essay is a bit too long.  Please make sure it's 300 words or less.")

# Validators for applicant scores 
min_score_validator = MinValueValidator(0, message="The score can't be lower than 0")
max_score_validator = MaxValueValidator(10, message="The score can't be higher than 10")



# Idea model, associated with users (a user can have many ideas)
class Idea(models.Model):
	idea_text = models.CharField(null=False, 
															 verbose_name="Idea Text",
															 max_length=255)



class Candidate(models.Model):
	# Possible roles, plus tuple w/tuples for options 
	DESIGNER = "DES"
	DEVELOPER = "DEV"
	ROLES = (
		(DESIGNER, "Designer"),
		(DEVELOPER, "Developer"),
	)

	# Role
	role = models.CharField(max_length=3,
													choices=ROLES, 
													default=DEVELOPER,
													verbose_name="Role")

	# Essay (300 words or less)
	essay = models.CharField(null=True, 
													 blank=True, 
													 verbose_name="Candidate Essay",
													 validators=[validate_essay_length],
													 max_length=100000)

	# Access Code (to view via URL); set in the form 
	access_code = models.CharField(null=False,
																 blank=True, 
																 verbose_name="Rand64 Access Code",
																 max_length=64)

	# Score validators 
	min_score_validator = MinValueValidator(0, message="The score can't be lower than 0")
	max_score_validator = MaxValueValidator(10, message="The score can't be higher than 10")


	# Score to rate applicants to the core team (0-10)
	score = models.IntegerField(null=True, 
															blank=True, 
															verbose_name="Preference Score",
															validators=[min_score_validator, max_score_validator])

	# Status, where notes can be made about the applicant 
	# based on interview performance, application submission strength, 
	# coding/training program performance, etc. 
	status = models.CharField(null=True, 
														blank=True, 
														verbose_name="Status Notes",
														max_length=255) 




class Trainee(models.Model): 

	# Essay (300 words or less)
	essay = models.CharField(null=True,
													 blank=True, 
													 verbose_name="Trainee Essay",
													 validators=[validate_essay_length],
													 max_length=100000)

	# Access Code (to view via URL); set in the form 
	access_code = models.CharField(null=False,
																 blank=True, 
																 verbose_name="Rand64 Access Code",
																 max_length=64)

	# Score to rate training program applicants (0-10)
	scores = models.IntegerField(null=True,
															 blank=True, 
															 verbose_name="Preference Score",
															 validators=[min_score_validator, max_score_validator])


	# Status notes, based on training program application (0-10)
	status = models.CharField(null=True,
														blank=True, 
														verbose_name="Status Notes",
														max_length=255)





# Primary model created when someone signs up for the email list, 
# an idea, or submits an application for the team or the training program 
class AppDevUser(models.Model): 


	# First Name
	first_name = models.CharField(null=False, 
																verbose_name="First Name", 
																max_length=40)


	# Last Name
	last_name = models.CharField(null=False, 	
															 verbose_name="Last Name",
															 max_length=60)


	# To check the email's form 
	email_validator = RegexValidator(regex="[A-Za-z]{2,3}[0-9]{1,5}@cornell.edu")


	# Email 
	email = models.EmailField(null=False,
														max_length=25,
														unique=True,
														validators=[email_validator], 
														verbose_name="Email") # Email validator will be run to validate this field 

	# On email list or not 
	on_email_list = models.BooleanField(verbose_name="On Email List?") 


	# Year validators 
	max_year_validator = MaxValueValidator(2019, message="The year specified is too high")
	min_year_validator = MinValueValidator(2016, message="The year specified is too low")


	# Year 
	year = models.IntegerField(verbose_name="Year", 
														 null=True, 
														 validators=[max_year_validator, min_year_validator])


	# Major 
	major = models.CharField(max_length=60, null=True)


	# Highest course validators 
	max_course_validator = MaxValueValidator(7000, message="The course number you entered is too high")
	min_course_validator = MinValueValidator(1000, message="The course number you entered is too low")


	# Highest CS Course 
	highest_cs_course = models.IntegerField(verbose_name="Highest CS Course",
																					null=True,
																					validators=[max_course_validator, min_course_validator])


	# Ideas are a separate model 
	ideas = models.ManyToManyField(Idea)



	# Candidate foreign key
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)



	# Trainee foreign key
	trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)



	# Link to resume (via Dropbox or Google Docs or something)
	resume_link = models.CharField(null=True, 
																 blank=True,
																 max_length=200,
																 verbose_name="Resume Link")


	# Portfolio link (for Github, design portfolio, personal website, etc.)
	portfolio_link = models.CharField(null=True, 
																 		blank=True,
																 		max_length=200,
																 		verbose_name="Portfolio Link")





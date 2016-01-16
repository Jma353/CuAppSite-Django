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

# Highest course validators 
max_course_validator = MaxValueValidator(7000, message="The course number you entered is too high")
min_course_validator = MinValueValidator(1000, message="The course number you entered is too low")




# Idea model, associated with users (a user can have many ideas)
class Idea(models.Model):
	idea_text = models.CharField(null=False, 
															 verbose_name="Idea Text",
															 max_length=255)


# To add the access_code to the create method 
class ApplicantManager(models.Manager): 
	def create(self, **kwargs): 
		access_code = generate_random_key(64)
		return super(ApplicantManager, self).create(access_code=access_code, *args, **kwargs)




# Trainee 
# DB Schema information
# role: 							string, `DES` or `DEV`, indicating the role of the applicant 
# essay: 							string, can be blank, <= 300 words w/custom validator 
# portfolio_link: 		string, can be blank, max 200 chars 
# resume_link: 				string, can be blank, max 200 chars
# access_code: 				random 64 character string, SET IN THE FORM 
# score: 							integer, 0-10, can be null/blank, used to rank core-team apps 
# status: 						string, can be null/blank, max 255 chars, used to keep notes on core-team app/interview 

class Candidate(models.Model):
	# For access_code generation 
	objects = ApplicantManager() 


	# Possible roles, plus tuple w/tuples for options 
	DESIGNER = "DES"
	DEVELOPER = "DEV"
	ROLES = (
		(DESIGNER, "Designer"),
		(DEVELOPER, "Developer"),
	)

	# Role
	role = models.CharField(max_length=20,
													choices=ROLES, 
													default=DEVELOPER,
													verbose_name="Role")


	# Essay (300 words or less)
	essay = models.CharField(blank=False,
													 default="", 
													 verbose_name="Candidate Essay",
													 validators=[validate_essay_length],
													 max_length=100000)


	# Portfolio link (for Github, design portfolio, personal website, etc.)
	portfolio_link = models.CharField(blank=False,
																		default="", 
																 		max_length=200,
																 		verbose_name="Portfolio Link")


	# Link to resume (via Dropbox or Google Docs or something)
	resume_link = models.CharField(null=True, 
																 blank=False,
																 max_length=200,
																 verbose_name="Resume Link")


	# Access Code (to view via URL); set in the form 
	access_code = models.CharField(null=False,
																 blank=True, 
																 verbose_name="Rand64 Access Code",
																 max_length=64)

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




# Trainee 
# DB Schema information

# highest_cs_course: 	integer, can be null, <=7000, >=1000
# essay: 							string, can't be blank, <= 300 words w/custom validator 
# portfolio_link: 		string, can't be blank, max 200 chars 
# resume_link: 				string, can't be blank, max 200 chars
# access_code: 				random 64 character string, SET IN THE FORM 
# score: 							integer, 0-10, can be null/blank, used to rank trainee apps 
# status: 						string, can be null/blank, max 255 chars, used to keep notes on trainee app 


class Trainee(models.Model): 
	# For access_code generation  
	objects = ApplicantManager() 

	# Highest CS Course 
	highest_cs_course = models.IntegerField(verbose_name="Highest CS Course",
																					null=True,
																					validators=[max_course_validator, min_course_validator])


	# Essay (300 words or less)
	essay = models.CharField(blank=False, 
													 default="",
													 verbose_name="Trainee Essay",
													 validators=[validate_essay_length],
													 max_length=100000)


	# Portfolio link (for Github, design portfolio, personal website, etc.)
	portfolio_link = models.CharField(blank=False,
																		default="", 
																 		max_length=200,
																 		verbose_name="Portfolio Link")


	# Link to resume (via Dropbox or Google Docs or something)
	resume_link = models.CharField(null=True, 
																 blank=False,
																 max_length=200,
																 verbose_name="Resume Link")


	# Access Code (to view via URL); set in the form 
	access_code = models.CharField(null=True, # So it can be validated via the form properly 
																 blank=True, 
																 verbose_name="Rand64 Access Code",
																 max_length=64)

	# Score to rate training program applicants (0-10)
	score = models.IntegerField(null=True,
															 blank=True, 
															 verbose_name="Preference Score",
															 validators=[min_score_validator, max_score_validator])


	# Status notes, based on training program application (0-10)
	status = models.CharField(null=True,
														blank=True, 
														verbose_name="Status Notes",
														max_length=255)



# AppDevUser 

# DB Schema information
# first_name: 				string, can't be null, max 40 chars 
# last_name: 					string, can't be null, max 60 chars 
# email: 							email, regex validator, max 25 chars * 
# on_email_list: 			boolean, default False 
# submitted_tp:				boolean, default False (a.k.a. submitted training program app)
# submitted_ct: 			boolean, default False (a.k.a. submitted core team app)
# year: 							integer, can be null, >=2016, <=2019
# major: 							string, can be null, max 60 chars 
# ideas: 							many-to-many relationship 
# candidate: 					foreign-key relationship 
# trainee: 						foreign-key relationship 

# * the email should be unique, but this is handled via all forms 


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
														validators=[email_validator], 
														verbose_name="Email") # Email validator will be run to validate this field 

	# On email list or not 
	on_email_list = models.BooleanField(verbose_name="On Email List?", default=False) 

	# Submitted training program app? 
	submitted_tp = models.BooleanField(verbose_name="Submitted Training Program App?", default=False)

	# Submitted core team app? 
	submitted_ct = models.BooleanField(verbose_name="Submitted Core Team App?", default=False)


	# Year validators 
	max_year_validator = MaxValueValidator(2019, message="The year specified is too high")
	min_year_validator = MinValueValidator(2016, message="The year specified is too low")


	# Year 
	year = models.IntegerField(verbose_name="Year", 
														 null=True, 
														 validators=[max_year_validator, min_year_validator])


	# Major 
	major = models.CharField(max_length=60, null=True)



	# Ideas are a separate model 
	ideas = models.ManyToManyField(Idea)



	# Candidate foreign key
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)



	# Trainee foreign key
	trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, null=True)


	# String representation 
	def __str__(self): 
		return self.first_name + " " + self.last_name + " | " + self.email




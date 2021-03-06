from django import forms 
from applications.models import Candidate, Trainee, AppDevUser 
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.models import User # For the purposes of logging in the admin 
import helpers # Helper functions


class EmailForm(forms.ModelForm): 	
	""" Form used for adding users to the email list on the home page and on the footer """

	def clean_email(self):
		cleaned_data = self.cleaned_data 
		try:
			AppDevUser.objects.get(email=cleaned_data['email']) 
			# IF ABOVE IS SUCCESSFUL, THEN ALREADY ON EMAIL LIST 
			raise forms.ValidationError("This email already exists in our database.")
		except ObjectDoesNotExist: 
			return self.cleaned_data['email']

	# NOT CALLED ON FIELD, CALLED ON THE FORM 
	# Attempts to populate first_name and last_name fields via web-scraping 
	def clean(self):
		# Get the data that has been run through validations 
		cleaned_data = self.cleaned_data 

		try: email = cleaned_data['email']
		except KeyError: raise forms.ValidationError("No email was entered.")

		first_name = helpers.get_first_name(email) 

		# Catching this issue early 
		if first_name == None: # Will be none if not found 
			self.cleaned_data['first_name'] = ""
			self.cleaned_data['last_name'] = ""
 
		last_name = helpers.get_last_name(email)

		self.cleaned_data['first_name'] = first_name
		self.cleaned_data['last_name'] = last_name


	

	class Meta:

		model = AppDevUser
		fields = ['email'] # Just the email list 





class UserForm(forms.ModelForm):
	""" General form for user information """ 



	class Meta: 
		model = AppDevUser
		fields = ['first_name', 'last_name', 'email', 'year', 'major']

		# Using this to indicate what type of input I want 
		help_texts = {
			'first_name': 'text',
			'last_name': 'text',
			'email': 'email',
			'year': 'number',
			'major': 'text',
		}

		widgets = {
			'first_name': forms.TextInput(attrs={ 'placeholder': 'John', 'class': 'form-control' }),
			'last_name': forms.TextInput(attrs={ 'placeholder': 'Doe', 'class': 'form-control' }),
			'email': forms.EmailInput(attrs={ 'placeholder': 'jd222@cornell.edu', 'class': 'form-control' }),
			'year': forms.NumberInput(attrs={ 'placeholder': 2019, 'class': 'form-control' }),
			'major': forms.TextInput(attrs={ 'placeholder': 'Computer Science', 'class': 'form-control' }),
		}

class CandidateForm(forms.ModelForm):

	""" Form for Core Team Candidate """

	class Meta: 
		model = Candidate

		fields = ['role', 'essay', 'portfolio_link', 'resume_link']

		help_texts = {}

		widgets = {
			'role': forms.Select(attrs={  'class': 'form-control' }),
			'essay': forms.Textarea(attrs={ 'placeholder': 'Things to include: Highest CS course (for devs), relevant experience, reason(s) for wanting to join the team, and why you\'d rock as member of CU App Dev!',
																		  'class': 'form-control essay', 'rows': 10 }),
			'portfolio_link': forms.TextInput(attrs={ 'placeholder': 'Github (for devs), Dropbox link, a personal site, etc.', 
																								'class': 'form-control' }),
			'resume_link': forms.TextInput(attrs={ 'placeholder': 'Resume via Google Drive, Dropbox, etc.', 
																						 'class': 'form-control' }),
		}


class TraineeForm(forms.ModelForm):
	""" Form for Training Program Applicants """

	class Meta: 
		model = Trainee 
		fields = ['highest_cs_course', 'essay', 'portfolio_link', 'resume_link']

		help_texts = {}

		widgets = {
			'highest_cs_course': forms.NumberInput(attrs={ 'placeholder': '1110 (or 1000 if you have not taken a CS class at Cornell, just so we know)', 'class': 'form-control'}),
			'essay': forms.Textarea(attrs={ 'placeholder': 'Things to include: Why you are interested in learning iOS programming, ' + 
																									 'what experience you have with iOS app development/programming in general, and why you think you our Training Program will benefit you.', 
																			'class': 'form-control essay', 'rows': 10 }),
			'portfolio_link': forms.TextInput(attrs={ 'placeholder': 'Github, Dropbox link, a personal site, etc.', 
																								'class': 'form-control' }),
			'resume_link': forms.TextInput(attrs={ 'placeholder': 'Resume via Google Drive, Dropbox, etc.', 
																						 'class': 'form-control' }),
		}

class AdminForm(forms.ModelForm):
	""" Form used to log into basic admin portal """ 

	class Meta: 
		model = User 
		fields = ['username', 'password']
		help_texts = {}

		widgets = {
			'username': forms.TextInput(attrs={ 'class': 'form-control' }),
			'password': forms.PasswordInput(attrs={ 'class': 'form-control' })
		}


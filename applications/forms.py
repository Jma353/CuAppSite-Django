from django import forms 
from applications.models import Candidate, Trainee, AppDevUser 
import helpers # Helper functions




class EmailForm(forms.ModelForm): 	
	""" Form used for adding users to the email list on the home page and on the footer """

	# This type of validation only performed on first name b/c 
	# last_name will be `None` if first_name is `None` 
	def clean_first_name(self):
		# How one would typically get this data
		email = self.cleaned_data['email']

		first_name = helpers.get_first_name(email)

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
		fields = ['email']









# Need an email form

# Need a candidate form that creates a user and then a candidate from that user 

# Need a training program form that creates a user and then a trainee from that user 

# NEED TO READ UP ON FORM VALIDATIONS AGAIN AND MODEL VALIDATING VIA CLEAN AND SUCH 




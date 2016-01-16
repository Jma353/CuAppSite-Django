import random
import string
from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect 
from django.template import loader 
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView # Generic view used for generating forms
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist 
from applications.forms import EmailForm, UserForm, CandidateForm
from applications.models import AppDevUser

# Each static page has a email submission on it somewhere 
# In BaseStaticView, define functionality to handle this email submission

# NOTE: ALL POST REQUESTS FOR THE FOOTER EMAIL FORM ARE MADE TO "/"


# For the access code of Candidate and Trainee 
def generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


class BaseStaticView(FormView): 
	form_class = EmailForm

	# On POST request (form submission)
	def post(self, request): 
		print request.POST # POST request 
		form = EmailForm(request.POST) # Populate the email form with the values submitted 
		if form.is_valid(): 
				u = form.save(commit=False)
				u.on_email_list = True
				u.save()
				return JsonResponse({ "success": "Thanks for your email! We'll keep you in the loop!" })
		else: 
			print form.errors.as_json
			return JsonResponse(form.errors.as_json(escape_html=True), safe=False)


class Home(BaseStaticView): 
	# On a GET request 
	def get(self, request): 
		# loader.get_template() --> template 
		# template.render(context, request) passed into HttpResponse --> proper 
		template = loader.get_template('home.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request)) 

	# POST defined above


class AboutUs(BaseStaticView): 
	def get(self, request):
		template = loader.get_template('about_us.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class ContactUs(BaseStaticView): 
	def get(self, request): 
		template = loader.get_template('contact_us.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Apply(BaseStaticView):
	def get(self, request):
		template = loader.get_template('apply.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Learn(BaseStaticView):
	def get(self, request):
		template = loader.get_template('learn.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Legal(BaseStaticView):
	def get(self, request):
		template = loader.get_template('legal.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Sponsors(BaseStaticView):
	def get(self, request):
		template = loader.get_template('sponsors.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Team(BaseStaticView):
	def get(self, request):
		template = loader.get_template('team.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Projects(BaseStaticView):
	def get(self, request):
		template = loader.get_template('projects.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class Application(BaseStaticView): 

	def get(self, request): 
		template = loader.get_template('application.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class TPSuccess(BaseStaticView): 

	def get(self, request):
		template = loader.get_template('tp-success.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


class CTSuccess(BaseStaticView):

	def get(self, request): 
		template = loader.get_template('ct-success.html')
		context = { 'request': request, 'form': self.form_class, 'email_form': self.form_class }
		return HttpResponse(template.render(context, request))


# Essentially, combines several forms, and responds to post requests made to 
# THIS URL SPECIFICALLY 
class TrainingProgram(FormView):

	user_form = UserForm(prefix="user")
	 
	email_form = EmailForm


	def get(self, request):
		template = loader.get_template('training-program.html')
		context = { 'request': request, 
								'user_form': self.user_form, 
								'email_form': self.email_form 
							} 
		return HttpResponse(template.render(context, request))





class CoreTeam(FormView):

	email_form = EmailForm()

	# Sets up appropriate forms w/proper prefixes for the purposes of validating 
	# two forms on a single post request... one for the user, one for the candidate 
	# associated with the user 
	user_form = UserForm(prefix="user")
	candidate_form = CandidateForm(prefix="candidate")

	partially_saved_user = None 

	def get(self, request):
		template = loader.get_template('core-team.html')
		context = { 'request': request, 
								'email_form': self.email_form, 
								'user_form': self.user_form, 
								'candidate_form': self.candidate_form
							} 

		return HttpResponse(template.render(context, request))


	# This contains a lot of repeated code, possibly refactor given time constraints  
	def post(self, request):
		print request.POST
		# Submitted forms w/appropriate data 
		submitted_user_form = UserForm(request.POST, prefix="user")
		submitted_candidate_form = CandidateForm(request.POST, prefix="candidate")

		if all([submitted_user_form.is_valid(), submitted_candidate_form.is_valid()]): 
			u_cleaned_data = submitted_user_form.cleaned_data
			c_cleaned_data = submitted_candidate_form.cleaned_data
			user_email = u_cleaned_data['email']

			try: 
				u = AppDevUser.objects.get(email=user_email)
				if u.submitted_ct: # Already submitted core-team application
					messages.info(request, "You already submitted a Core Team app.")
					return HttpResponseRedirect(reverse('core-team-success'))
				else: # This email exists, but a ct-app has not been submitted 
					u.delete() # Delete old user instance 
					u = submitted_user_form.save(commit=False)
					u.on_email_list = True 
					u.submitted_ct = True 
					c = submitted_candidate_form.save(commit=False)
					c.access_code = generate_random_key(64)
					c.save() 
					u.candidate = c
					u.save() 
					messages.info(request, "Thank you for applying to our Core Team!")
					return HttpResponseRedirect(reverse('core-team-success'))
			except ObjectDoesNotExist as e: # No user exists with that email 
				u = submitted_user_form.save(commit=False) # Save the user
				u.on_email_list = True 
				u.submitted_ct = True 
				c = submitted_candidate_form.save(commit=False)
				c.access_code = generate_random_key(64)
				c.save() 
				u.candidate = c
				u.save() 
				messages.info(request, "Thank you for applying to our Core Team!")
				return HttpResponseRedirect(reverse('core-team-success'))	

		else: 
			return render(request, 'core-team.html', {
				'request': request,
				'email_form': self.email_form,
				'user_form': submitted_user_form,
				'candidate_form': submitted_candidate_form
			}); 




		# In this view, we need to create a user from the user fields that are filled, create a 
		# candidate object associated with the user, generate a random value for checking 
		# the basic information of that user via the admin panel, etc. 


		# All values not featured in the form must be instantied properly 


		# As a default, we must also create a trainee object with filled in information, b/c all
		# people not accepted onto the full team are automatically referred to the training program 










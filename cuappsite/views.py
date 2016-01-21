import random
import string
from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect 
from django.template import loader 
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView # Generic view used for generating forms
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist 
from applications.forms import EmailForm, UserForm, CandidateForm, TraineeForm, AdminForm 
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


# To see if a user exists 
def user_exists(cleaned_data):
	email = cleaned_data['email']
	try: 
		u = AppDevUser.objects.get(email=email)
		return u 
	except ObjectDoesNotExist as e: 
		return None


# To save a user with a specific attr as well 
def save_user_via_form(user_form, attr_form, attr):
	if attr == "candidate": 
		submitted = "submitted_ct"
	elif attr == "trainee": 
		submitted = "submitted_tp"

	u = user_form.save(commit=False) 
	u.on_email_list = True
	setattr(u, submitted, True)
	attr_obj = attr_form.save(commit=False)
	attr_obj.access_code = generate_random_key(64)
	attr_obj.save() 
	setattr(u, attr, attr_obj)
	u.save() 




# Essentially, combines several forms, and responds to post requests made to 
# THIS URL SPECIFICALLY 
class TrainingProgram(FormView):

	email_form = EmailForm()

	# Prefixed separate form processing 
	user_form = UserForm(prefix="user")
	trainee_form = TraineeForm(prefix="trainee") 

	def get(self, request):
		template = loader.get_template('training-program.html')
		context = { 'request': request, 
								'email_form': self.email_form,
								'user_form': self.user_form, 
								'trainee_form': self.trainee_form
							} 
		return HttpResponse(template.render(context, request))


	def post(self, request):
		print request.POST
		# Submitted forms w/appropriate data 
		submitted_user_form = UserForm(request.POST, prefix="user")
		submitted_trainee_form = TraineeForm(request.POST, prefix="trainee")

		if all([submitted_user_form.is_valid(), submitted_trainee_form.is_valid()]): 
			u_cleaned_data = submitted_user_form.cleaned_data
			t_cleaned_data = submitted_trainee_form.cleaned_data
			u = user_exists(u_cleaned_data)
			if u != None: 
				if u.submitted_tp:
					messages.info(request, "You already submitted a Core Team App.")
					return HttpResponseRedirect(reverse('core-team-success'))
				else: 
					u.delete()
					save_user_via_form(submitted_user_form, submitted_trainee_form, "trainee")
					messages.info(request, "Thank you for applying to our Training Program")
					return HttpResponseRedirect(reverse('training-program-success'))
			else: 
				save_user_via_form(submitted_user_form, submitted_trainee_form, "trainee")
				messages.info(request, "Thank you for applying to our Training Program!")
				return HttpResponseRedirect(reverse('training-program-success'))		

		else: 
			return render(request, 'training-program.html', {
				'request': request,
				'email_form': self.email_form,
				'user_form': submitted_user_form,
				'trainee_form': submitted_trainee_form
			}); 






class CoreTeam(FormView):

	email_form = EmailForm()

	# Sets up appropriate forms w/proper prefixes for the purposes of validating 
	# two forms on a single post request... one for the user, one for the candidate 
	# associated with the user 
	user_form = UserForm(prefix="user")
	candidate_form = CandidateForm(prefix="candidate")

	def get(self, request):
		template = loader.get_template('core-team.html')
		context = { 'request': request, 
								'email_form': self.email_form, 
								'user_form': self.user_form, 
								'candidate_form': self.candidate_form
							} 

		return HttpResponse(template.render(context, request))


	def post(self, request):
		print request.POST
		# Submitted forms w/appropriate data 
		submitted_user_form = UserForm(request.POST, prefix="user")
		submitted_candidate_form = CandidateForm(request.POST, prefix="candidate")

		if all([submitted_user_form.is_valid(), submitted_candidate_form.is_valid()]): 
			u_cleaned_data = submitted_user_form.cleaned_data
			c_cleaned_data = submitted_candidate_form.cleaned_data
			u = user_exists(u_cleaned_data)
			if u != None: 
				if u.submitted_ct:
					messages.info(request, "You already submitted a Core Team App.")
					return HttpResponseRedirect(reverse('core-team-success'))
				else: 
					u.delete()
					save_user_via_form(submitted_user_form, submitted_candidate_form, "candidate")
					messages.info(request, "Thank you for applying to our Core Team!")
					return HttpResponseRedirect(reverse('core-team-success'))
			else: 
				save_user_via_form(submitted_user_form, submitted_candidate_form, "candidate")
				messages.info(request, "Thank you for applying to our Core Team!")
				return HttpResponseRedirect(reverse('core-team-success'))		

		else: 
			return render(request, 'core-team.html', {
				'request': request,
				'email_form': self.email_form,
				'user_form': submitted_user_form,
				'candidate_form': submitted_candidate_form
			}); 





def sandbox(request):
	template = loader.get_template('sandbox.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))



class AdminLogin(FormView):
	form_class = AdminForm

	def get(self, request):
		template = loader.get_template('admin/admin-login.html')
		context = { 'request': request, 'admin_form': self.form_class }
		return HttpResponse(template.render(context, request))




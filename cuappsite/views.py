from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect 
from django.template import loader 
from django.views.generic.edit import FormView # Generic view used for generating forms
from applications.forms import EmailForm

# Each static page has a email submission on it somewhere 
# In BaseStaticView, define functionality to handle this email submission

class BaseStaticView(FormView): 
	form_class = EmailForm

	# On POST request (form submission)
	def post(self, request): 
		print request.POST # POST request 
		form = EmailForm(request.POST) # Populate the email form with the values submitted 
		if form.is_valid(): 
			print form.cleaned_data.get('email')
			print form.cleaned_data.get('first_name')
			print form.cleaned_data.get('last_name')
			return JsonResponse({ "success": "Thanks for your email! We'll keep you in the loop!" })
		else: 
			for x in form.errors.keys(): 
				print form.errors[x].as_text

			return JsonResponse({ "failure": "One or more errors occurred.  Please re-enter your email."})


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


class TrainingProgram(FormView):

	def get(self, request):
		template = loader.get_template('training-program.html')
		context = { 'request': request, 'form': EmailForm, 'email_form': EmailForm } # Will change 
		return HttpResponse(template.render(context, request))


class CoreTeam(FormView):

	def get(self, request):
		template = loader.get_template('core-team.html')
		context = { 'request': request, 'form': EmailForm, 'email_form': EmailForm } # Will change 
		return HttpResponse(template.render(context, request))






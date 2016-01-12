from django.shortcuts import render 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect 
from django.template import loader 

# List of static pages 

def home(request): 
	# loader.get_template() --> template 
	# template.render(context, request) passed into HttpResponse --> proper 
	template = loader.get_template('home.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request)) 

def about_us(request): 
	template = loader.get_template('about_us.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))

def contact_us(request): 
	template = loader.get_template('contact_us.html')
	context = { 'request': request } 
	return HttpResponse(template.render(context, request))

def apply(request): 
	template = loader.get_template('apply.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))

def learn(request): 
	template = loader.get_template('learn.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))

def legal(request): 
	template = loader.get_template('legal.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))

def sponsors(request):
	template = loader.get_template('sponsors.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))

def team(request):
	template = loader.get_template('team.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))


def projects(request):
	template = loader.get_template('projects.html')
	context = { 'request': request }
	return HttpResponse(template.render(context, request))



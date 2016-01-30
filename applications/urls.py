from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views 

app_name = 'applications'

# For admin view (REST API)
urlpatterns = [
	url(r'^applicant/(?P<email>[A-Za-z]*[0-9]*@cornell.edu)/$', views.ApplicantDetail.as_view()),
]

# This allows for the .json, .xml etc. extensions 
urlpatterns = format_suffix_patterns(urlpatterns)
"""cuappsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^about_us/', views.AboutUs.as_view(), name='about_us'), 
    url(r'^contact_us/', views.ContactUs.as_view(), name='contact_us'), 
    url(r'^apply/', views.Apply.as_view(), name='apply'), 
    url(r'^learn/', views.Learn.as_view(), name='learn'),
    url(r'^legal/', views.Legal.as_view(), name='legal'), 
    url(r'^sponsors/', views.Sponsors.as_view(), name='sponsors'),
    url(r'^team/', views.Team.as_view(), name='team'), 
    url(r'^projects/', views.Projects.as_view(), name='projects'),
    url(r'^$', views.Home.as_view(), name='home'), 
]

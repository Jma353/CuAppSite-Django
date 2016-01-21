from django.contrib import admin
from applications.models import AppDevUser, Candidate, Trainee, Idea 

admin.site.register(AppDevUser)
admin.site.register(Candidate)
admin.site.register(Trainee)
admin.site.register(Idea)
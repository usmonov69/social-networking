from django.contrib import admin
from .models import Profile, Relationship

admin.site.register(Relationship)
admin.site.register(Profile)
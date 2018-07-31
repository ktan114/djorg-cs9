from django.contrib import admin
from .models import Note, PersonalNote

admin.site.register((Note, PersonalNote))
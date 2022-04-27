from django.contrib import admin
from django.contrib.admin.decorators import display

# Register your models here.
from . import models

class AuthorAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','content')
admin.site.register(models.Post,AuthorAdmin)

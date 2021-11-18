from django.contrib import admin
from .models import BlogPost, Categories, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

admin.site.register(Categories)
admin.site.register(BlogPost, SummernoteModelAdmin)
admin.site.register(Comment)

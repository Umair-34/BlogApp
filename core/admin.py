from django.contrib import admin
from .models import BlogPost, Categories, Comment
# Register your models here.

admin.site.register(Categories)
admin.site.register(BlogPost)
admin.site.register(Comment)

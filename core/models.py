from django.db import models
from accounts.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.urls import reverse


# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class BlogPost(models.Model):
    title = models.CharField(max_length=450)
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    img = models.ImageField(upload_to='blog', null=True)
    blog = models.TextField(max_length=50000)
    post_date = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, blank=True, on_delete=models.PROTECT, related_name='category_set')
    upvote = models.ManyToManyField(User, related_name='blog_liked', blank=True)
    Approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def total_upvote(self):
        return self.upvote.count()

    def total_upvote(self):
        return self.upvote.count()

    def get_absolute_url(self):
        return reverse('core:DetailView', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title + " | " + self.author.first_name + " " + self.author.last_name


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

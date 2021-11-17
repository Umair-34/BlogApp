from django.db import models
from accounts.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager


# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Comment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sender.first_name + " " + self.sender.last_name


class BlogPost(models.Model):
    title = models.CharField(max_length=450)
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    img = models.ImageField(upload_to='blog', null=True)
    blog = models.TextField(max_length=10000)
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set')
    upvote = models.ManyToManyField(User, related_name='blog_liked', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def total_upvote(self):
        return self.upvote.count()

    def __str__(self):
        return self.title + " | " + self.author.first_name + " " + self.author.last_name

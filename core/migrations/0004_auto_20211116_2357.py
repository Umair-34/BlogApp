# Generated by Django 3.2.9 on 2021-11-16 23:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_blogpost_upvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, to='core.Comment'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='upvote',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-20 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='Approved',
            field=models.BooleanField(default=False),
        ),
    ]
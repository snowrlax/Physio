# myapp/models.py
from django.db import models

# Before

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    # Add other fields as needed

class saveEmail(models.Model):
    Email = models.EmailField()

class CustomUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(unique=True)


# Up

class userinfo(models.Model):
    username = models.CharField(max_length=50)
    game1 = models.IntegerField()
    game2 = models.IntegerField()
    game3 = models.IntegerField()
    game4 = models.IntegerField()


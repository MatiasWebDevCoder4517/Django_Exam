from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        now = date.today()
        print(now)
        i = postData['date_birth'].split('-')
        i = date(int(i[0]), int(i[1]), int(i[2]))

        ''' age = i[0] - 16  # 2021 - 16 = 2005
        if i[0] >= age:
            errors["date_birth"] = "You must be over 16 years to registrate!" '''

        if i >= now:
            errors["date_birth"] = "Date Birth can not be in the future or equal!"

        if len(postData['name']) < 4:
            errors["name"] = "Name name should be at least 4 or more characters"

        if len(postData['alias']) < 4:
            errors["alias"] = "Alias name should be at least 4 or more characters"

        if len(postData['password']) < 8:
            errors["password"] = "Password must be a minimum length of eight characters!"

        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords must match!"

        if User.objects.filter(alias=postData['alias']):
            errors["alias"] = "Alias already exist!"

        if len(postData['email']) < 7:
            errors["email"] = "Email should be at least 4 or more characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email must be a valid email address!"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255, default="user_name")
    alias = models.CharField(max_length=255, default="user_alias")
    email = models.EmailField(
        max_length=100, default="user_email123@gmail.com")
    password = models.CharField(max_length=255)
    date_birth = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name
##################################################################################
class FriendshipManager(models.Manager):
    pass
    ''' def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 4:
            errors["name"] = "Name name should be at least 4 or more characters"
        return errors '''


class Friendship(models.Model):
    ''' name = models.CharField(max_length=255, default='Charlie') '''
    friendship = models.ForeignKey(
        User, related_name="my_friend", on_delete=models.CASCADE)
    friends_users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FriendshipManager()

    def __str__(self):
        return self.name, self.friendship.user

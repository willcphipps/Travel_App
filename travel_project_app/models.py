from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
import re
import bcrypt



class UsersManager(models.Manager):
#registraion validation--------------------------------------------
    def register_validator(self, postData):
        errors = {}

        if len(postData['fname']) < 1:
            errors["fname"] = "First Name must be at least two characters"
        if len(postData['lname']) < 1:
            errors["lname"] = "Last Name must be at least two characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email address must be valid."
        (postData['email'])
        if len(self.filter(email=postData['email'])) > 0:
            errors["email"] = "You already have an account!"
        if len(postData['password']) < 7:
            errors["password"] = "Password must be at least eight characters long"
        if (postData['confirm']) != (postData['password']):
            errors["confirm"] = "Passwords must match"
        return errors
#login validation---------------------------------------------------
    def login_validator(self, postData):
        errors = {}
        
        if len(self.filter(email=postData['email'])) < 1:
            errors['email'] = "You are not a registered user"
        elif len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
                errors['password'] = "Wrong Password"
        return errors
class DestinationsManager(models.Manager):
#adding destination validation--------------------------------------------
    def add_new_validator(self, postData):
        errors = {}

        if len(postData['destination']) < 3:
            errors["destination"] = "You must have a destination!"
        if postData['start'] == '':
            errors["start"] = "Must enter a date!"
        if postData['end'] == ' ':
            errors["end"] = "Must enter a date!"
        if len(postData['plan']) < 3:
            errors["destination"] = "You must have a plan!"
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    objects = UsersManager()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Destinations(models.Model):
    destination = models.CharField(max_length=45)
    travelers = models.ManyToManyField(Users, related_name="joined_trips")
    start_date = models.CharField(max_length=45)
    end_date = models.CharField(max_length=45)
    plan = models.CharField(max_length=200)
    objects = DestinationsManager()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip_admin = models.ForeignKey(Users, related_name="created_trips", on_delete=models.CASCADE)

from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
now = str(datetime.now())


class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}
        if len(form['name']) == 0:
            errors['name'] = 'Name is required'
        elif len(form['name']) < 3:
            errors['name'] = 'Name must be at least three characters long'

        if len(form['username']) == 0:
            errors['username'] = 'Username is required'
        elif len(form['username']) < 3:
            errors['username'] = 'Username must be at least three characters long'
        else:
            users = User.objects.filter(username=form['username'])
            if users:
                errors['username'] = "Username already exists"

        if len(form['password']) == 0:
            errors['password'] = 'Password is required'
        elif len(form['password']) < 8:
            errors['password'] = 'Password must be at least eight characters long'
        if form['confirm_password'] != form['password']:
            errors['confirm_password'] = 'Passwords do not match'

        return errors

    def loginValidator(self, form):
            errors = {}
            if len(form['password']) == 0:
                errors['password'] = 'Password cannot be blank'
            if len(form['username']) == 0:
                errors['username'] = 'Username cannot be blank' 
            else:
                users = User.objects.filter(username=form['username'])
                if not users:
                    errors['username'] = 'This user doesnt exist. Please register'
                elif not bcrypt.checkpw(form['password'].encode(), users[0].password.encode()):
                    errors['password'] = 'Wrong password'
            return errors




class DestinationManager(models.Manager):
    def destinationValidator(self, form):
        print(form)
        errors = {}     
        
        if len(form['city']) == 0:
            errors['city'] = 'City is required'
        elif len(form['city']) < 2:
            errors['city'] = 'City must be at least two characters long'

        if len(form['destination_description']) == 0:
            errors['destination_description'] = 'Description is required'

        if len(form['start_date']) == 0:
            errors['start_date'] = 'Please enter date'
        elif form['start_date'] < now:
            errors['start_date'] = 'Must be in the future'
        
        if len(form['end_date']) == 0:
            errors['end_date'] = 'Please enter date'
        elif form['end_date'] < form['start_date']:
            errors['end_date'] = 'Cannot return in the pass'
            
        return errors


class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Destination(models.Model):
    city = models.CharField(max_length=45)
    start_date=models.DateField()
    end_date=models.DateField()
    destination_description=models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='destination', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DestinationManager()
    

class Join(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, related_name='favorites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def loginValidator(self, form):
        errors = {}
        if len(form['loginpassword']) == 0:
            errors['loginpassword'] = 'Password is required'
        if len(form['loginusername']) == 0:
            errors['loginusername'] = 'Username is required' 
        else:
            users = User.objects.filter(username=form['username'])
            if not users:
                errors['loginusername'] = 'This username doesnt exist. Please register'
            elif not bcrypt.checkpw(form['password'].encode(), users[0].password.encode()):
                errors['loginpassword'] = 'Wrong password'
        return errors
        
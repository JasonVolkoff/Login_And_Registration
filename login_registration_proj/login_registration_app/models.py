from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def validation(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            errors['firstName'] = 'First Name must be at least 2 characters'
        if len(form['lastName']) < 2:
            errors['lastName'] = 'Last Name must be at least 2 characters'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid email address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if form['password'] != form['confirmPassword']:
            errors['password'] = 'Passwords do not match'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(),
                           bcrypt.gensalt()).decode()
        return self.create(
            first_name=form['firstName'],
            last_name=form['lastName'],
            email=form['email'],
            password=pw
        )


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()

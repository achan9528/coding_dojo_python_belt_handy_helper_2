from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstName']) < 2:
            errors['firstName'] = "First Name should be at least 2 characters!"
        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last Name should be at least 2 characters!"
        if not EMAIL_REGREX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Invalid email - user already exists!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['passwordConfirm']:
            errors['passwordConfirm'] = "Password does not match!"
        return errors
        
    def loginValidator(self, postData):
        errors = {}
        EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGREX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) < 1:
            errors['email'] = "Invalid email address - user does not exist. Please register!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        return errors

    def userInfoValidator(self, postData):
        errors = {}
        EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGREX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['firstName']) < 2:
            errors['firstName'] = "Invalid First Name!"
        if len(postData['lastName']) < 2:
            errors['lastName'] = "Invalid Last Name!"
        return errors

    def userPasswordValidator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        return errors

class TaskManager(models.Manager):
    def inputValidator(self,postData):
        errors = {}

        if len(postData['title']) < 3:
            errors['title'] = "Task Title should be at least 3 characters!"
        if len(postData['title']) == 0:
            errors['title'] = "Task Title must be provided!"
        if len(postData['desc']) < 3:
            errors['desc'] = "Task Description should be at least 3 characters!"
        if len(postData['desc']) == 0:
            errors['desc'] = "Task Description must be provided!"
        if len(postData['location']) < 3:
            errors['location'] = "Task Location should be at least 3 characters!"
        if len(postData['location']) == 0:
            errors['location'] = "Task Location must be provided!"
        
        return errors

class CategoryManager(models.Manager):
    def inputValidator(self,postData):
        errors = {}
        inPostData = False
        for category in Category.objects.all():
            if category.title in postData:
                inPostData = True
        
        print(inPostData)
        print(postData)
        if inPostData==False and postData['categoryOther']=="":
            errors['category'] = "Please select a category or enter a new one!"

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    #tasksAdded = tasks that the User has added
    #tasksOwned = tasks that the User has said they would do 

class Category(models.Model):
    title = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = CategoryManager()
    #tasksAssociated = tasks associated with the category

    def __str__(self):
        return f"Category title: {self.title}"

class Task(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    addedBy = models.ForeignKey(User, related_name="tasksAdded", on_delete=models.CASCADE)
    objects = TaskManager()
    owner = models.ForeignKey(User, related_name="tasksOwned", on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category, related_name="tasksAssociated", null=False)
    isCompleted = models.BooleanField(default=False)
    #isCompleted = boolean field (black belt)
    #owner = foreign key user object (black belt)
    #categories = categories that the task falls under, many to many field (black belt)

    def __str__(self):
        return f"Task Owner: {self.owner}"

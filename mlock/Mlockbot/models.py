from django.db import models

# Create your models here.

class Mlockbot(models.Model):
    id= models.AutoField
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    id= models.AutoField
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Orders(models.Model):
    id= models.AutoField
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Outcome(models.Model):
    id= models.AutoField
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
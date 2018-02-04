from django.db import models

# Create your models here.

class Accounts(models.Model):
    lschet = models.IntegerField(primary_key=True)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    addressSTR = models.CharField(max_length=500)
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    planstruct = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=50)
    flat = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    person =  models.IntegerField();
    space = models.FloatField(default=0)

    def __str__(self):
        return self.lschet+'/'+self.surname+' '+self.name+ ' '+self.patronymic

class Settlements(models.Model):
    lschet = models.IntegerField(primary_key=True)
    Service = models.CharField(max_length=50)

    def __str__(self):
        return self.lschet+'/'+self.surname+' '+self.name+ ' '+self.patronymic
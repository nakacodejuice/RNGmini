from django.db import models

# Create your models here.

class Request(models.Model):

    uid = models.CharField(max_length=36, primary_key=True)
    method = models.CharField(max_length=100)
    params = models.TextField()
    compress = models.BooleanField()
    debug = models.BooleanField()
    json = models.BooleanField()
    isdead = models.BooleanField(default=False)
    datetime = models.DateTimeField('date created', auto_now_add=True)
    isresponsed = models.BooleanField(default=False)

    def __str__(self):
        return self.method+'/'+self.datetime

class Response(models.Model):

    uid = models.CharField(max_length=36, primary_key=True)
    resp = models.TextField()
    method = models.CharField(max_length=100)
    datetime = models.DateTimeField('date created', auto_now_add=True)
    isresponsed = models.BooleanField(default=False)

    def __str__(self):
        return self.method+'/'+self.datetime

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Transform(models.Model):
    file_name = models.TextField()
    channel = models.IntegerField()
    wavelet = models.ImageField(upload_to='media')
    standart_cardio = models.ImageField(upload_to='media')

class TestWavelet(models.Model):
    wavelet = models.ImageField(upload_to='test/media')
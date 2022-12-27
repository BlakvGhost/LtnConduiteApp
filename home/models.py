from django.db import models
from django.contrib.auth.models import User

class Vote(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    vote_date = models.DateTimeField(auto_now_add=True, null=False)
    classe = models.CharField(max_length=255, null=True, blank=False)
    niveau = models.CharField(max_length=255, null=True, blank=False)
    note = models.CharField(max_length=255, null=True, blank=False)
    message = models.TextField(null=True, blank=False)
    ua = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.classe

class Classe(models.Model):
    classe = models.CharField(max_length=255, null=True, blank=False)
    note = models.CharField(max_length=255, null=True, blank=False)
    niveau = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.classe

class AskNewPassword(models.Model):
    user = models.IntegerField(default=0)
    email = models.EmailField(max_length=255, null=True, blank=False)
    message = models.TextField(null=True, blank=False)
    statue = models.CharField(max_length=30, null=True, blank=False)
    ua = models.CharField(max_length=255, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.statue

class Review(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=False)
    content = models.TextField(null=True, blank=False)
    statue = models.CharField(max_length=30, null=True, blank=False)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.rate

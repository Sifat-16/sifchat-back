from operator import mod
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='my_profile', blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

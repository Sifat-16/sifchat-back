
from django.db import models
from account.models import *
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class MyThreadManager(models.Manager):
    def by_profile(self, profile):
        q_lookup1 = Q(first=profile) | Q(second=profile)
        q_lookup2 = Q(first=profile) & Q(second=profile)
        qs = self.get_queryset().filter(q_lookup1).exclude(q_lookup2).distinct()
        return qs


class MyThread(models.Model):
    first = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chat_thread_first")
    second = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chat_thread_second")
    latest_message = models.ForeignKey(
        'ChatMessage', on_delete=models.SET_NULL, null=True, blank=True, related_name="lm")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MyThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    class Meta:
        ordering = ['-updated']


class ChatMessage(models.Model):
    mythread = models.ForeignKey(
        MyThread, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.ForeignKey(
        UserProfile, verbose_name="sender", on_delete=models.CASCADE)
    message = models.TextField()
    snap = models.ImageField(upload_to='chat_images', blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)


# @receiver(post_save, sender=ChatMessage)
# def save_thread_latest(sender: ChatMessage, instance, created, **kwargs):
#     if created:

#         mth = MyThread.objects.get(id=instance.mythread.id)
#         mth.latest_message = instance
#         mth.save()
#         print("saved")
#         return mth
#         # instance.mythread.save()

from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
# from auditlog.registry import auditlog
# from auditlog.models import AuditlogHistoryField
# from django.conf import settings
# from django.dispatch import receiver
# from django.db.models.signals import (
#     pre_save,
#     post_save,
#     pre_delete,
#     post_delete,
#     m2m_changed,
# )

# User1 = settings.AUTH_USER_MODEL
User = get_user_model()

# Create your models here.


# @receiver(pre_save, sender=User1)
# def user_pre_save_receiver(sender, instance, *args, **kwargs):
#     """
#     before saved in the database
#     """
#     print(instance.username, instance.id) # None

# @receiver(post_save, sender=User)
# def user_post_save_receiver(sender, instance, created, *args, **kwargs):
#     """
#     after saved in the database
#     """
#     if created:
#         print("Send email to", instance.username)
#     else:
#         print(instance.username, "was just saved")

        
MEDIA_CHOICES = [
    ('1', "Image"),
    ('2', "Video"),
    ('3', "Text"),
]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=70, null=True)
    type_of_media = models.CharField(max_length=100,choices = MEDIA_CHOICES,default = '1')
    media = models.BinaryField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)
    # history = AuditlogHistoryField()


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # history = AuditlogHistoryField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    # history = AuditlogHistoryField()



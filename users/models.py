from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

import uuid


def avatar_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    og_filename = filename.split('.')[0]
    new_filename = "avatar_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg', upload_to=avatar_dir_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
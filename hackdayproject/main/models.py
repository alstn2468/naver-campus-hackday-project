from django.db import models
from django.conf import settings


class Repository(models.Model):
    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    repo_name = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    pushed_at = models.DateTimeField(auto_now=False, auto_now_add=False)

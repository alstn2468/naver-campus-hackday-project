from django.db import models
from django.conf import settings
from hackdayproject.utils.github_api import get_user_data


class Repository(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=100)
    language = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()

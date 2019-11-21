from django.db import models
from django.conf import settings


class Repository(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    owner = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, primary_key=True)
    language = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()

    def __str__(self):
        return self.full_name.split("/")[1]


class Commit(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE
    )
    sha = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    date = models.DateTimeField()

    def __str__(self):
        return self.sha


class Organization(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    orgs_name = models.CharField(max_length=100, primary_key=True)
    avatar_url = models.TextField()

    def __str__(self):
        return self.orgs_name

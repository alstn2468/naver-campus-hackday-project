from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from hackdayproject.utils.github_api import get_user_data


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    avatar_url = models.TextField()
    company = models.CharField(max_length=50, blank=True)
    blog_url = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    public_repos_count = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        user_data = get_user_data(username)

        if type(user_data) is dict:
            Profile.objects.create(
                user=instance,
                avatar_url=user_data["avatar_url"],
                company=user_data["company"],
                blog_url=user_data["blog_url"],
                location=user_data["location"],
                bio=user_data["bio"],
                public_repos_count=user_data["public_repos_count"],
                followers=user_data["followers"],
                following=user_data["following"]
            )

        else:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserLoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='login_logs',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address')
    )
    user_agent = models.CharField(
        verbose_name=_('HTTP User Agent'),
        max_length=300,
    )

    class Meta:
        verbose_name = _('user login log')
        verbose_name_plural = _('user login logs')
        ordering = ('-created',)

    def __str__(self):
        return '%s %s' % (self.user, self.ip_address)

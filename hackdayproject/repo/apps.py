from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RepoConfig(AppConfig):
    name = 'repo'
    verbose_name = _('Repo')

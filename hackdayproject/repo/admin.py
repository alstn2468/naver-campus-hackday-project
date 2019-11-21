from django.contrib import admin
from hackdayproject.repo.models \
    import Repository, Commit, Organization

admin.site.register(Repository)
admin.site.register(Commit)
admin.site.register(Organization)

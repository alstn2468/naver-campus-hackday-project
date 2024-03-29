from django.urls import path, include
from django.contrib import admin
import hackdayproject.main.urls as main_urls
import hackdayproject.repo.urls as repo_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', include(main_urls)),
    path('repo/', include(repo_urls))
]

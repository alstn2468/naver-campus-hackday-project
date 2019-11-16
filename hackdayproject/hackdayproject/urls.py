from django.urls import path, include
from django.contrib import admin
import hackdayproject.main.urls as main_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_urls))
]

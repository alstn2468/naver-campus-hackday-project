from django.urls import path
from django.contrib.auth import views as auth_views
from hackdayproject.main import views as main_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('login/', main_views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', main_views.settings, name='settings'),
    path('settings/password/', main_views.password, name='password'),
]

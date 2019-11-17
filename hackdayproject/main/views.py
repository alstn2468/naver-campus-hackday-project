from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.conf import settings as conf_settings
import requests


def home(request):
    user = request.user

    if user:
        try:
            GIT_API_URL = conf_settings.GIT_API_URL
            suffix = "?client_id=" + conf_settings.SOCIAL_AUTH_GITHUB_KEY + \
                "&client_secret=" + conf_settings.SOCIAL_AUTH_GITHUB_SECRET

            user_data = requests.get(
                GIT_API_URL + "/users/" + user.username + suffix).json()

            user_data = {
                "avatar_url": user_data["avatar_url"],
                "company": user_data["company"],
                "blog_url": user_data["blog"],
                "location": user_data["location"],
                "bio": user_data["bio"],
                "public_repos_count": user_data["public_repos"],
                "followers": user_data["followers"],
                "following": user_data["following"]
            }

            # Get all public repo according to public_repos_count
            user_repos = requests.get(
                GIT_API_URL + '/users/' + user.username + '/repos' + suffix
                + '&per_page=' + str(user_data["public_repos_count"]), {
                    "type": "all",
                    "sort": "updated"
                }).json()

            user_repos = [repos["full_name"] for repos in user_repos]

        except Exception as e:
            print(e)
            user_data = {
                "error": "Can't get user data."
            }

    return render(request, 'main/home.html', {
        "user_data": user_data,
        "user_repos": user_repos
    })


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'main/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)

    return render(request, 'main/password.html', {'form': form})

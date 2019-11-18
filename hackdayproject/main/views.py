from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms \
    import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from hackdayproject.utils.github_api \
    import get_user_data, get_user_repos


def home(request):
    user = request.user

    if user:
        user_data = get_user_data(user.username)

        if "dict" == type(user_data):
            user_repos = get_user_repos(
                user.username, str(user_data["public_repos_count"])
            )

        else:
            user_repos = "Can't get user repository data."

    return render(request, 'main/home.html', {
        "user_data": user_data,
        "user_repos": user_repos,
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

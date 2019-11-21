from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from hackdayproject.main.forms import MyLoginForm, MyPasswordChangeForm
from hackdayproject.utils.util_function \
    import convert_to_localtime, string_date_to_datetime
from collections import OrderedDict
from datetime import timedelta


def home(request):
    user = request.user

    commit_logs = {}

    if user.is_authenticated:
        repos = user.repository_set.all()

        for repo in repos:
            commits = repo.commit_set.all()

            for commit in commits:
                date = str(convert_to_localtime(commit.date))[:10]

                if date in commit_logs.keys():
                    commit_logs[date] += 1

                else:
                    commit_logs[date] = 1

        commit_logs = OrderedDict(
            sorted(commit_logs.items(), key=lambda t: t[0]))

        commit_logs = list(commit_logs.items())
        before_commit = string_date_to_datetime(commit_logs[0][0])
        current_streak = 0

        for i in range(1, len(commit_logs)):
            now_commit = string_date_to_datetime(commit_logs[i][0])
            commit_day_diff = (now_commit - before_commit).days

            if commit_day_diff == 1:
                current_streak += 1
            else:
                print("before", before_commit, "now", now_commit)
                current_streak = 0
            before_commit = now_commit

        print(current_streak)

    return render(request, 'main/home.html', {
        "commit_logs": commit_logs
    })


class MyLoginView(auth_views.LoginView):
    form_class = MyLoginForm


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
        PasswordForm = MyPasswordChangeForm
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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from hackdayproject.utils.github_api import get_user_data, get_user_orgs
from hackdayproject.main.models import Profile
from hackdayproject.repo.models import Repository
from social_django.models import UserSocialAuth
from hackdayproject.main.forms import MyLoginForm, MyPasswordChangeForm
from hackdayproject.utils.util_function import get_user_all_repo


def home(request):
    user = request.user

    if user.is_authenticated:
        username = user.username

        if not hasattr(user, "profile"):
            user_data = get_user_data(username)
            profile = Profile(
                user=user,
                avatar_url=user_data["avatar_url"],
                company=user_data["company"],
                blog_url=user_data["blog_url"],
                location=user_data["location"],
                bio=user_data["bio"],
                public_repos_count=user_data["public_repos_count"],
                followers=user_data["followers"],
                following=user_data["following"]
            )
            profile.save()

        orgs_data = get_user_orgs(username)
        user_repo = get_user_all_repo(username, orgs_data)

        for repo in user_repo:
            repository = Repository(
                user=user,
                full_name=repo["full_name"],
                owner=repo["owner"],
                language=repo["language"],
                description=repo["description"],
                created_at=repo["created_at"],
                updated_at=repo["updated_at"],
                pushed_at=repo["pushed_at"]
            )
            repository.save()
    else:
        orgs_data = "AnonymousUser"

    return render(request, 'main/home.html', {
        "orgs_data": orgs_data
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

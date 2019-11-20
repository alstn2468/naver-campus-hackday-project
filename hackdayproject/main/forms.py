import unicodedata
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms \
    import PasswordChangeForm, AuthenticationForm


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("이전 비밀번호"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Before Password'
        })
    )
    new_password1 = forms.CharField(
        label=_("새로운 비밀번호"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        label=_("새로운 비밀번호 확인"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password Check'
        })
    )


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
        }


class MyLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm


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

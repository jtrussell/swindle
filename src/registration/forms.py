from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'u-full-width'})
        self.fields['email'].widget.attrs.update({'class': 'u-full-width'})
        self.fields['password'].widget.attrs.update({'class': 'u-full-width'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'u-full-width'})
        self.fields['email'].widget.attrs.update({'class': 'u-full-width'})

    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discord_handle'].widget.attrs.update(
            {'class': 'u-full-width'})

    class Meta:
        model = UserProfile
        fields = ('discord_handle', )

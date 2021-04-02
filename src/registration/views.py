from django.shortcuts import render
from .forms import UserForm, UserProfileForm

# Create your views here.

# Create your views here.
def profile(request):
    return render(request, 'registration/profile.html')


def sign_up(request):
    user_form = UserForm()
    profile_form = UserProfileForm()
    return render(request, 'registration/sign-up.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
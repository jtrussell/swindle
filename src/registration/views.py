from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, UpdateUserForm, UserProfileForm

# Create your views here.

# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def sign_up(request):
    user_form = NewUserForm()
    profile_form = UserProfileForm()
    return render(request, 'registration/sign-up.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

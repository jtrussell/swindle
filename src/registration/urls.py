from . import views
from django.urls import path


urlpatterns = [
    path('', views.profile, name='profile'),
    path('sign-up', views.sign_up, name='show_sign_up_form')
]


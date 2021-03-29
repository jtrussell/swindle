from . import views
from django.urls import path


urlpatterns = [
    path('boards/<slug:group_slug>/', views.leaderboard_group,
         name='show_group'),
    path('board/<slug:leaderboard_slug>/',
         views.leaderboard_detail, name='show_leaderboard'),
    path('board/<slug:leaderboard_slug>/new-challenge',
         views.new_challenge, name='show_challenge_form'),
    path('board/<slug:leaderboard_slug>/challenge/<int:challenge_id>',
         views.challenge_detail, name='show_challenge'),
    path('board/<slug:leaderboard_slug>/results',
         views.result_list, name='show_results'),
    path('board/<slug:leaderboard_slug>/results/<int:result_id>',
         views.result_detail, name='show_result'),
    path('result', views.submit_result, name='submit_result'),
]

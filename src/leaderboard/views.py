from django.shortcuts import render
from .models import Challenge
from .models import Competitor
from .models import CompetitorDeck
from .models import Deck
from .models import Leaderboard
from .models import LeaderboardGroup


# Create your views here.
def index(request):
    return render(request, 'leaderboard/index.html')


def leaderboard_group(request, group_slug):
    group = LeaderboardGroup.objects.filter(
        slug=group_slug).first()
    return render(request, 'leaderboard/leaderboard-group.html', {
        'leaderboard_group': group,
    })


def leaderboard_detail(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    return render(request, 'leaderboard/leaderboard-detail.html', {
        'leaderboard': board,
    })


def leaderboard_history(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    return render(request, 'leaderboard/leaderboard-history.html', {
        'leaderboard': board,
    })


def new_challenge(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    return render(request, 'leaderboard/new-challenge.html', {
        'leaderboard': board,
    })


def challenge_detail(request, leaderboard_slug, challenge_id):
    return render(request, 'leaderboard/index.html')


def result_detail(request, leaderboard_slug, result_id):
    return render(request, 'leaderboard/index.html')

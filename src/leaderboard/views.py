from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Challenge
from .models import Competitor
from .models import CompetitorDeck
from .models import Deck
from .models import Leaderboard
from .models import LeaderboardGroup
from .models import Result
from .forms import LeaderboardChallengeForm, ResultForm, get_result_form_for_challenge


# Create your views here.
def index(request):
    return render(request, 'leaderboard/index.html')

def leaderboard_groups(request):
    groups = LeaderboardGroup.objects.all()
    return render(request, 'leaderboard/leaderboard-groups.html', {
        'leaderboard_groups': groups,
    })


def leaderboard_group(request, group_slug):
    group = LeaderboardGroup.objects.filter(
        slug=group_slug).first()
    return render(request, 'leaderboard/leaderboard-group.html', {
        'leaderboard_group': group,
    })


def leaderboard_detail(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    form = LeaderboardChallengeForm()
    return render(request, 'leaderboard/leaderboard-detail.html', {
        'leaderboard': board,
        'form': form,
    })


def new_challenge(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    if request.method == 'POST':
        form = LeaderboardChallengeForm(request.POST)
        if form.is_valid():
            mv_id = Deck.get_mv_id_from_url(form.cleaned_data['deck_url'])
            # TODO - get SAS and deck name from DoK
            # Also, update the "submit_claim" handler
            deck_sas = form.cleaned_data['deck_sas']
            deck_name = form.cleaned_data['deck_name']

            # Upsert DECK
            deck, created = Deck.objects.update_or_create(
                mv_id=mv_id,
                defaults={'name': deck_name}
            )

            # Create competitor
            competitor = Competitor.objects.create(
                user=request.user,
                leaderboard=board
            )

            # Create competitor Deck
            competitor_deck = CompetitorDeck.objects.create(
                competitor=competitor,
                deck=deck,
                sas=deck_sas
            )

            # Create challenge or claim this board
            if board.champion:
                challenge = Challenge.objects.create(
                    created_by=competitor,
                    leaderboard=board
                )
            else:
                board.champion = competitor
                board.champion_since = None
                board.champion_winning_streak = 0
                board.save()

            return redirect(board)

    else:
        form = LeaderboardChallengeForm()

    return render(request, 'leaderboard/challenge-new.html', {
        'leaderboard': board,
        'form': form,
    })


def challenge_detail(request, leaderboard_slug, challenge_id):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    challenge = Challenge.objects.get(id=challenge_id)
    form = get_result_form_for_challenge(challenge)
    return render(request, 'leaderboard/challenge-detail.html', {
        'leaderboard': board,
        'challenge': challenge,
        'form': form,
    })


@require_POST
@login_required
def submit_result(request):
    form = ResultForm(request.POST)
    if form.is_valid():
        challenge = form.cleaned_data.challenge
        allow_submit = challenge.is_user_allowed_to_submit_results(
            request.user)
        if allow_submit:
            result = form.save()
            winner = result.winner
            board = result.leaderboard
            if winner == board.champion:
                board.champion_winning_streak = board.champion_winning_streak + 1
            else:
                board.champion = winner
                board.champion_since = result
                board.board.champion_winning_streak = 1
            board.save()
            return redirect(result)
    return HttpResponseNotFound()


def result_list(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    return render(request, 'leaderboard/result-list.html', {
        'leaderboard': board,
    })


def result_detail(request, leaderboard_slug, result_id):
    result = Result.objects.get(id=result_id)
    return render(request, 'leaderboard/result-detail.html', {
        'result': result,
    })

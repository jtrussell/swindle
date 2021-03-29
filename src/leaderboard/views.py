from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
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


def new_challenge(request, leaderboard_slug):
    board = Leaderboard.objects.filter(slug=leaderboard_slug).first()
    if request.method == 'POST':
        form = LeaderboardChallengeForm(request.POST)
        if form.is_valid():
            mv_id = Deck.get_mv_id_from_url(form.cleaned_data['deck_url'])
            # TODO - get SAS and deck name from DoK
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

            # Create challenge
            challenge = Challenge.objects.create(
                created_by=competitor,
                leaderboard=board
            )

            # TODO - redirect to the challenge (gotta have pages for challenges fist ;))
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


def submit_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        # TODO validate user is allowed to submit this result!
        if form.is_valid():
            result = form.save()
            return redirect(result)
        else:
            print('Form is not valid')
            # TODO shouldn't ever happen... but redirect somewhere better
            print(form.errors)
            return HttpResponseNotFound()
    else:
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

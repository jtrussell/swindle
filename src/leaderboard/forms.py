from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Deck, Result, Competitor
import uuid


def deck_url_validator(value):
    try:
        mv_id = Deck.get_mv_id_from_url(value)
        mv_uuid = uuid.UUID(mv_id)
    except ValueError:
        raise(ValidationError(
            _('Deck link is invalid'),
            code='invalid'
        ))


class LeaderboardChallengeForm(forms.Form):
    deck_url = forms.CharField(
        max_length=200,
        label=_('Deck link'),
        validators=[deck_url_validator],
        widget=forms.TextInput(attrs={
            'placeholder': _('DoK or Master Vault'),
            'class': 'u-full-width',
        }))
    deck_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'u-full-width',
        }))
    deck_sas = forms.IntegerField(
        max_value=150,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'u-full-width',
        }))


def get_result_form_for_challenge(challenge):
    competitor_ids = [challenge.created_by.id]
    if challenge.leaderboard.champion is not None:
        competitor_ids.append(challenge.leaderboard.champion.id)

    class ChallengeResultForm(forms.ModelForm):
        winner = forms.ModelChoiceField(
            Competitor.objects.filter(id__in=competitor_ids),
            widget=forms.RadioSelect
        )

        class Meta:
            model = Result
            fields = ('winner', 'leaderboard', 'challenge', 'defended_by')
            widgets = {
                'leaderboard': forms.HiddenInput(),
                'challenge': forms.HiddenInput(),
                'defended_by': forms.HiddenInput(),
            }
    return ChallengeResultForm(initial={
        'leaderboard': challenge.leaderboard,
        'challenge': challenge,
        'defended_by': challenge.leaderboard.champion,
    })


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = ('winner', 'leaderboard', 'challenge', 'defended_by')

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Deck
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

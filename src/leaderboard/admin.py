from django.contrib import admin
from .models import Challenge
from .models import Competitor
from .models import CompetitorDeck
from .models import Deck
from .models import Leaderboard
from .models import LeaderboardGroup


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'leaderboard', 'created_on')


class CompetitorAdmin(admin.ModelAdmin):
    pass


class CompetitorDeckAdmin(admin.ModelAdmin):
    list_display = ('deck', 'sas', 'competitor')


class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'mv_id')


class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',), }


class LeaderboardGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(CompetitorDeck, CompetitorDeckAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Leaderboard, LeaderboardAdmin)
admin.site.register(LeaderboardGroup, LeaderboardGroupAdmin)

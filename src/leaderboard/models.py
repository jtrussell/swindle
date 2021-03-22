from django.db import models
from django.contrib.auth.models import User


class LeaderboardGroup(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    sort_order = models.IntegerField()
    group = models.ForeignKey(
        LeaderboardGroup, on_delete=models.CASCADE, related_name='leaderboards')
    champion = models.ForeignKey(
        'Competitor', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='+')
    champion_since = models.ForeignKey(
        'Result', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='+')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']


class Deck(models.Model):
    mv_id = models.UUIDField(unique=True)
    name = models.CharField(max_length=200)


class Competitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()


class CompetitorDeck(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    sas = models.IntegerField(default=0)


class Challenge(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']


RESULT_STATUES = (
    (0, "Completed"),
    (1, "Archived"),
)


class Result(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, null=True, blank=True)
    defended_by = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    status = models.IntegerField(choices=RESULT_STATUES, default=0)

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe


class LeaderboardGroup(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True)
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
    champion_winning_streak = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_leaderboard', kwargs={'leaderboard_slug': self.slug})

    def last_five_results(self):
        return Result.objects.filter(leaderboard=self)[:5]

    class Meta:
        ordering = ['sort_order']


class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    mv_id = models.UUIDField(unique=True)
    name = models.CharField(max_length=200)

    @staticmethod
    def get_mv_id_from_url(value):
        return value.strip().rsplit('/', 1)[-1]

    def __str__(self):
        return self.name

    def get_dok_url(self):
        return 'https://decksofkeyforge.com/decks/{}'.format(self.mv_id)


class Competitor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.id)

    def html(self):
        return mark_safe('<span class="competitor">{} <span class="text-muted">#{}</span></span>'.format(self.user.get_full_name(), self.id))


class CompetitorDeck(models.Model):
    id = models.AutoField(primary_key=True)
    competitor = models.ForeignKey(
        Competitor, on_delete=models.CASCADE, related_name='decks')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    sas = models.IntegerField(default=0)

    def __str__(self):
        return self.deck.name

    def get_dok_url(self):
        return self.deck.get_dok_url()


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE, related_name='challenges')

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse(
            'show_challenge',
            kwargs={
                'leaderboard_slug': self.leaderboard.slug,
                'challenge_id': self.id
            })

    def is_user_allowed_to_submit_results(self, user):
        # TODO - add a permission for admins to enter any results
        if user == self.created_by.user:
            return True
        try:
            if user == self.leaderboard.champion.user:
                return True
        except AttributeError:
            pass
        return False


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE, related_name='results')
    challenge = models.OneToOneField(
        Challenge, on_delete=models.CASCADE, null=True, blank=True)
    defended_by = models.ForeignKey(
        Competitor, on_delete=models.CASCADE, related_name='result_defenses')
    winner = models.ForeignKey(
        Competitor, on_delete=models.CASCADE, related_name='result_wins')

    def __str__(self):
        return 'Match #{}'.format(self.id)

    def html(self):
        return mark_safe('<span class="result">Match <span class="text-muted">#{}</span></span>'.format(self.id))

    def get_absolute_url(self):
        return reverse(
            'show_result',
            kwargs={
                'leaderboard_slug': self.leaderboard.slug,
                'result_id': self.id
            })

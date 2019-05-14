from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth.models import User
from .choices import *

# Create your models here.

# Use Django's built in User model to create user registrations and logins
# add unique constraint for email
# User.meta.get_field('email').unique = True
#
# # Require Email, first name, last name
# User.meta.get_field('email')._blank = False
# User.meta.get_field('first_name')._blank = False
# User.meta.get_field('last_name')._blank = False

# Create user authentication tokens upon creation


# Create user authentication tokens
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)


''' A player that owns sub cities 
    To streamline user input, and create first step of validation, 
    I made choices for constant variable names team and rank
    So that the users all select from the same drop down menu and the data retains consistency
'''


class Player (models.Model):

    # Every player has a username, a tag or tagless, and a rank. They also have a power, but that fluctuates by the
    # minute and would not be applicable without access to real time
    # create the models from the choices
    name = models.CharField(max_length=200, blank=False, unique=True)
    team = models.CharField(max_length=3, choices=TEAM_NAMES, default=None)
    rank = models.IntegerField(choices=RANKS, default=KNIGHT)

    # overwrite string method
    def __str__(self):
        return "Player {} Team {} Subs Allowed {}".format(self.name, self.team, self.rank)


''' One Sub City, owned by one user 
    Every Subcity has one of seven cultures. These cultures tell what added benefit they give a player. 
    Players want to store 3 pieces of information for a subcity - 
    who owns it(player), 
    where is it(coordinates), 
    what is it (culture + quality) '''


class Subcity (models.Model):

    # Only one sub city can occupy a paid of coordinates, so that is unique
    # A player can occupy more than one sub city, so that is not but it is a foreignKey
    coords = models.CharField(max_length=9, blank=False, unique=True)
    player = models.ForeignKey(Player, related_name='cities', blank=False, on_delete=models.CASCADE)
    culture = models.CharField(max_length=3, blank=False, choices=SUB_CULTURE, default=JAPAN)
    quality = models.CharField(max_length=6, blank=False, choices=SUB_QUALITY, default=EXCELLENT)

    # Overwrite String Method
    def __str__(self):
        return 'SUB CITY {} {} OWNED BY {} LOCATED {}'.format(self.quality, self.culture, self.player, self.coords)

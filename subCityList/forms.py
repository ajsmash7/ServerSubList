import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ValidationError
from django.utils.encoding import force_text

from .models import Player, Subcity

# Validator for coords field for data integrity


class CoordValidator(RegexValidator):
    regex = re.compile(r'/d/d/d/d,/d/d/d/d')
    message = "REQUIRED PATTERN = 0000,0000 ex. '52,378' should be '0052,0378' No spaces, no letters"
    code = 'invalid'
    inverse_match = False
    flags = 0

    def __call__(self, value):
        value = force_text(value)

        regex_matches = self.regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message, code=self.code)

    # def __eq__(self, other):
    #     return (
    #             isinstance(other, CoordValidator) and
    #             (self.regex.pattern == other.regex.pattern) and
    #             (self.message == other.message) and
    #             (self.code == other.code)
    #     )

    def validate_coords(self, value):
        if self.regex.match(value):
            return True
        else:
            raise ValidationError(self.message)


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30,
#                                widget=forms.TextInput(attrs=)
#     password = forms.CharField(label="Password", max_length=30,
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


# create new city record
class CityForm(forms.ModelForm):
    coords = forms.CharField(label='Coordinates', max_length=9, validators=[CoordValidator])

    class Meta:
        model = Subcity
        fields = ('coords', 'culture', 'quality')

    # Validate that city coordinates have not already been assigned

    def clean_coords(self):
        coordinates = self.clean_data['coords']

        city = Subcity.objects.filter(coords__iexact=coordinates).first()

        if not coordinates:
            raise ValidationError('Coordinates entered incorrectly. Pattern 0000,0000')

        if city:
            owner = city.player.name
            raise ValidationError('City is already owned by ' + owner)

        return coordinates

    # def save(self, commit=True):
    #     new_city= super(CityForm, self).save(commit=False)
    #     new_city.coords = self.cleaned_data['coords']
    #     new_city.culture = self.cleaned_data['culture']
    #     new_city.quality = self.cleaned_data['quality']
    #
    #     if commit:
    #         new_city.save()
    #
    #     return new_city


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'team', 'rank')

    def clean_name(self):

        name = self.cleaned_data['username']

        if not name:
            raise ValidationError('Please enter a username')

        if Player.objects.filter(name__iexact=name).exists():
            raise ValidationError('A user with that username already exists')

        return name


class SearchPlayerForm(forms.Form):
    search_name = forms.CharField(label='Enter Player Name', max_length=200)

    def clean_name(self):
        name = self.cleaned_data['name']

        if not name:
            raise ValidationError('Please enter a search name ')

        return name


class SearchCoordsForm(forms.Form):
    search_term = forms.CharField(label='Search Coordinates', max_length=9, validators=[CoordValidator.validate_coords])

# @login_required()
# class SearchTeamForm(forms.Forms):
#     DOA = 'DOA'
#     GRY = 'GRY'
#     GHO = 'GHO'
#     RIP = 'RIP'
#     BOB = 'BOB'
#     GNX = 'BOB'
#     EAD = 'EAD'
#     VN1 = 'VN1'
#     UTO = 'UTO'
#     TAGLESS = ' '  # it is possible for someone to be alone, not on a team. We call this being tagless.
#
#     TEAM_NAMES = (
#         (DOA, 'DOA'),
#         (GRY, 'GRY'),
#         (GHO, 'GHO'),
#         (RIP, 'RIP'),
#         (BOB, 'BOB'),
#         (GNX, 'GNX'),
#         (EAD, 'EAD'),
#         (VN1, 'VN1'),
#         (UTO, 'UTO'),
#         (TAGLESS, ' '),
#     )
#
#     search_team = forms.CharField(max_length=3, choices=TEAM_NAMES, default=None)


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_username(self):

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    # use the User model meta data
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    # save the editable changes for self.super User, for fields allowed to be edited. Notice password is excluded due
    # to Django password requirements
    # commit the changes to the form template

    def clean_username(self):

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class EditPlayerForm(UserChangeForm):

    # use the Player model meta data, display all fields
    class Meta:
        model = Player
        fields = ('name', 'team', 'rank')

    # verify that username is not empty, and that it is available
    def clean_name(self):

        name = self.cleaned_data['name']

        if not name:
            raise ValidationError('Please enter a username')

        if Player.objects.filter(name__iexact=name).exists():
            raise ValidationError('A user with that username already exists')

        return name

    # save the editable changes for self.super Player, for all fields, as they all can change at any time.
    # commit the changes to the form template
    def save(self, commit=True):
        player = super(EditPlayerForm, self).save(commit=False)
        player.name = self.cleaned_data['name']
        player.team = self.cleaned_data['team']
        player.rank = self.cleaned_data['rank']

        if commit:
            player.save()

        return player


# NOTE - I AM GOING TO MAKE THIS INTO A FORMSET - Once I figure out how
# It is considerably more efficient to edit the cities by player than it is individually
# So I want to create a formset that allows for multiple cities to be added and edited of one user
class EditCityOwner(UserChangeForm):

    class Meta:
        model = Subcity
        fields = ('coords', 'player', 'culture', 'quality')

    # Validate that player exists
    def clean_player(self):
        name = self.cleaned_data['player']

        if not name:
            raise ValidationError('Please enter a username')

        if Player.objects.filter(name__iexact=name).exists():
            player = Player.objects.filter(name__iexact=name).first()

            return player

    # save the editable changes for self.super, for owner field
    # commit the changes to the form template
    def save(self, commit=True):
        user = super(EditCityOwner, self).save(commit=False)

        if commit:
            user.save()

        return user


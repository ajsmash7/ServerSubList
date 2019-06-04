from django.shortcuts import render, redirect
from .models import Player, Subcity
from .forms import UserRegistrationForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

""" VIEWS FOR USER AND ACCOUNT TEMPLATES"""


def homepage(request):

    return render(request, 'subCityList/home.html')

# for redirect once logged in
@login_required
def my_user_profile(request):
    return redirect('subCityList:profile', user_pk=request.user.id)


# once a user logins, they are redirected to their profile, which contains a list of their own sub-cities
# User must register themselves as a player currently - not sure how to combine this with registration
def user_profile(request, user_pk):
    user = User.objects.get(id=user_pk)
    username = user.username
    player = Player.objects.filter(name__iexact=username).first()


    if player:
        cities = Subcity.objects.filter(player=player.id).order_by('quality')


    else:
        player = Player(name=username, team='GRY', rank=7)
        cities = Subcity.objects.filter(player=player.id).order_by('quality')

    return render(request, 'subCityList/user/profile.html', {'cities': cities, 'user': user, 'player': player})

# view to send edit form to template of specified user
# if form is not valid, display message and reload page
@login_required
def edit_user_profile(request):

    if request.method == 'POST':

        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('subCityList:user_profile', user_pk=request.user.id)

        else:
            message = 'Please check the changes you entered'
            return render(request, 'subCityList/user/edit_user_profile.html', {'form': form, 'message': message})

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'subCityList/user/edit_user_profile.html', {'form': form})


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('subCityList:homepage')

        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', {'form': form, 'message': message})

    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'subCityList/user/password.html', {'form': form})

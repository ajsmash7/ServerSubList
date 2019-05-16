from django.shortcuts import render, redirect
from .models import Player, Subcity
from .forms import UserRegistrationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

""" VIEWS FOR USER AND ACCOUNT TEMPLATES"""


def homepage(request):

    return render(request, 'home.html')

# for redirect once logged in
@login_required(login_url='/login/')
def my_user_profile(request):
    return redirect('profile.html', user_pk=request.user.pk)

# once a user logins, they are redirected to their profile, which contains a list of their own sub-cities
# User must register themselves as a player currently - not sure how to combine this with registration
def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    username = user.username
    player = Player.objects.filter(name=username).first()
    if player:
        cities = Subcity.objects.filter(player=player).order_by('quality')
        return render(request, 'profile.html', {'cities': cities, 'user': user})
    else:
        message = 'You are not a Player Yet!'
        return redirect('subCityList:player_add', {'message': message})

# view to send edit form to template of specified user
# if form is not valid, display message and reload page
@login_required(login_url='/login/')
def edit_user_profile(request):

    if request.method == 'POST':

        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('subCityList:user_profile', user_pk=request.user.pk)

        else:
            message = 'Please check the changes you entered'
            return render(request, 'edit_profile.html', {'form': form, 'message': message})

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('subCityList:my_user_profile')

        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', {'form': form, 'message': message})

    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})


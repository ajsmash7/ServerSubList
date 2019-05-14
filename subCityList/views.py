from django.shortcuts import render, redirect
from .models import Player, Subcity
from .forms import UserRegistrationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def homepage(request):

    return render(request, 'home.html')


@login_required(login_url='/login/')
def my_user_profile(request):
    return redirect('profile.html', user_pk=request.user.pk)


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
            return redirect('home.html')

        else:
            message = 'Please check the data you entered'
            return render(request, 'register.html', {'form': form, 'message': message})

    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})


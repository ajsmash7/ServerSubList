from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Subcity
from .forms import PlayerForm, SearchPlayerForm, EditPlayerForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def player_list(request):
    form = SearchPlayerForm()
    search_name = request.GET.get('search_name')

    if search_name:
        players = Player.objects.filter(name__icontains=search_name).order_by('name')
        return render(request, 'player_list.html', {'players': players, 'form': form, 'search_name': search_name})

    else:
        message = 'Player Not Found'
        return render(request, 'player_list.html', {'form': form, 'message': message, 'search_name': search_name})


def player_add(request):

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            return redirect('subCityList:player_detail', player_pk=player.pk)

    else:
        form = PlayerForm()

    return render(request, 'player_add.html', {'form': form})


def player_detail(request, player_pk):

    player = get_object_or_404(Player, pk=player_pk)
    cities = Subcity.objects.filter(player=player_pk).order_by('quality')
    return render(request, 'player_detail.html', {'player': player, 'cities': cities})


def player_edit(request, player_pk):

    player = get_object_or_404(Player, player_pk)

    if request.method == 'POST':

        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('subCityList:player_detail', player_pk=player.pk)

        else:
            message = 'Please check the changes you entered'
            return render(request, 'player_edit.html', {'form': form, 'message': message})

    else:
        form = EditPlayerForm(instance=player)
        return render(request, 'player_edit.html', {'form': form})

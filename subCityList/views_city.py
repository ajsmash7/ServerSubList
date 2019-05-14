from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Subcity
from .forms import CityForm, EditCityOwner, SearchCoordsForm


# Requires that the Player exist. If no player, will redirect to add one
def city_add(request, player_pk):
    player = get_object_or_404(Player, player_pk)

    if request.method == 'POST':
        form = CityForm(request.post)
        if form.is_valid():
            city = form.save(commit=False)
            city.player = player
            city.save()
            return redirect('subCityList:city_detail', city_pk=city.pk)

        else:
            message = 'Please check that the data entered is correct'
            return render(request, 'city_add.html', {'form': form, 'message': message})
    else:
        form = CityForm(instance=player)
        return render(request, 'city_add.html', { 'form': form })


def city_detail(request, city_pk):
    city = get_object_or_404(Subcity, city_pk)
    player_pk = city.player.pk
    player = get_object_or_404(Player, player_pk)
    return render(request, 'city_detail.html', {'city': city, 'player': player})


def city_view_all(request):
    players = Player.objects.all().order_by('name')
    return render(request, 'city_view_all.html', {'players': players})


def city_coords(request):
    form = SearchCoordsForm()
    search_term = request.GET.get('search_term')

    if search_term:
        city = Subcity.objects.filter(coords__iexact=search_term).first()
        return render(request, 'city_coords.html', {'city': city, 'form': form, 'search_term': search_term})

    else:
        message = 'City Not Found'
        return render(request, 'city_coords.html', {'form': form, 'message': message, 'search_term': search_term})


def city_edit(request, city_pk):
    city = get_object_or_404(Subcity, city_pk)
    player_pk = city.player.pk
    player = get_object_or_404(Player, player_pk)

    if request.method == 'POST':

        form = EditCityOwner(request.POST)
        if form.is_valid():

            form.save()
            return redirect('subCityList:city_detail', city_pk=city.pk)

        else:
            message = 'Player Not Found'
            return render(request, 'city_edit.html', {'form': form, 'message': message})

    else:
        form = EditCityOwner(instance=player)
        return render(request, 'city_edit.html', {'form': form, 'city_pk': city.pk} )




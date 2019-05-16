from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Subcity
from .forms import CityForm, EditCityOwner, SearchCoordsForm


# Requires that the Player exist. If no player, will redirect to add a player form template
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

# detail page of the attributes of one city.
# Requires the primary key of the specific city. If the city doesn't exist throw 404
# loads the information of the player who owns it as well.
def city_detail(request, city_pk):
    city = get_object_or_404(Subcity, city_pk)
    player_pk = city.player.pk
    player = get_object_or_404(Player, player_pk)
    return render(request, 'city_detail.html', {'city': city, 'player': player})

# view the entire list of all entered sub-cities
def city_view_all(request):
    cities = Subcity.objects.all().order_by('player')
    return render(request, 'city_view_all.html', {'cities': cities})

# Search city coordinates. If the search term is an exact match, display the first city returned
def city_coords(request):
    form = SearchCoordsForm()
    search_term = request.GET.get('search_term')

    if search_term:
        city = Subcity.objects.filter(coords__iexact=search_term).first()
        return render(request, 'city_coords.html', {'city': city, 'form': form, 'search_term': search_term})

    else:
        message = 'City Not Found'
        return render(request, 'city_coords.html', {'form': form, 'message': message, 'search_term': search_term})

# edit the owner of a cit. To do that, you'll also need the primary key of the player
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




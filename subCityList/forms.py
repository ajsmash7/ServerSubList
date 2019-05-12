from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Player, Subcity


# create new player using FormHelper
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'team', 'rank')

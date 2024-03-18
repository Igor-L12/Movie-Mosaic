# В вашем файле forms.py

from django import forms
from .models import ProductType

class GenreForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=ProductType.objects.all(), 
        empty_label=None, 
        label='Выберите жанр',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

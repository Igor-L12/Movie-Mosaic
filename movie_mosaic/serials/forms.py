from dal import autocomplete
from django import forms
from .models import ProductType, RatingSerial, RatingStar


class GenreForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=ProductType.objects.all(), 
        empty_label=None, 
        label='Выберите жанр',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class GenreButtonForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=ProductType.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'd-none'}),
        required=True
    )


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = RatingSerial
        fields = ("star",)
        

class BookmarkForm(forms.Form):
    movie_id = forms.IntegerField(widget=forms.HiddenInput())



from dal import autocomplete
from django import forms
from .models import ProductType, VideoProduct, Actor, Director, Release_Year, OriginalTitle, Rating, RatingStar


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
        model = Rating
        fields = ("star",)
        

class BookmarkForm(forms.Form):
    movie_id = forms.IntegerField(widget=forms.HiddenInput())

class VideoProductForm(forms.Form):
    title = forms.CharField(max_length=128, label='Название фильма в оригинале!')
    original_title = forms.CharField(max_length=128, label='Название фильма в русской локализации!')
    director = forms.CharField(max_length=128, label='Имя режиссера')
    actor = forms.CharField(max_length=128, label='Имя актёра')
    product_type = forms.CharField(max_length=128, label='Жанр')
    descriptions = forms.CharField(widget=forms.Textarea, label='Описание фильма')
    duration = forms.CharField(max_length=4, label='Продолжительность')
    release_year = forms.CharField(max_length=4, label='Год релиза')
    image = forms.ImageField(label='Обложка', required=False)

    def clean_original_title(self):
        original_title_name = self.cleaned_data.get('original_title')
        original_title, _ = OriginalTitle.objects.get_or_create(title=original_title_name)
        return original_title

    def clean_director(self):
        director_name = self.cleaned_data.get('director')
        director, _ = Director.objects.get_or_create(full_name=director_name)
        return director

    def clean_actor(self):
        actor_name = self.cleaned_data.get('actor')
        actor, _ = Actor.objects.get_or_create(full_name=actor_name)
        return actor

    def clean_product_type(self):
        product_type_name = self.cleaned_data.get('product_type')
        product_type, _ = ProductType.objects.get_or_create(title=product_type_name)
        return product_type

    def clean_release_year(self):
        year = self.cleaned_data.get('release_year')
        release_year, _ = Release_Year.objects.get_or_create(year=year)
        return release_year

    def save(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data['title']
        director = cleaned_data['director']
        actor = cleaned_data['actor']
        original_title = cleaned_data['original_title']
        product_type = cleaned_data['product_type']
        descriptions = cleaned_data['descriptions']
        duration = cleaned_data['duration']
        release_year = cleaned_data['release_year']
        image = cleaned_data.get('image')

        video_product = VideoProduct.objects.create(
            title=title,
            descriptions=descriptions,
            duration=duration,
            release_year=release_year,
            image=image,
            original_title=original_title
        )

        video_product.directors.add(director)
        video_product.actors.add(actor)
        video_product.product_type.add(product_type)
        video_product.save()



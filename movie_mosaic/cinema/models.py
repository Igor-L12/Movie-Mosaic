from django.db import models


class BaseModel(models.Model):
    """
    Абстрактная модель. 
    Добавляет к модели дату создания и последнего изменения. 
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:

        abstract = True 

class OriginalTitle(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Название фильма')

    class Meta():
        verbose_name='Название фильма'
        verbose_name_plural='Название фильмов'

    def __str__(self):
        return self.title

class ProductType(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Жанр')

    class Meta():
        verbose_name='Жанр'
        verbose_name_plural='Жанры'

    def __str__(self):
        return self.title

class Director(BaseModel):
    full_name = models.CharField(max_length=128, verbose_name='Имя режиссёра')

    class Meta():
        verbose_name='Режиссёр'
        verbose_name_plural='Режиссёры'

    def __str__(self):
        return self.full_name
    
class Actor(BaseModel):
    full_name = models.CharField(max_length=128, verbose_name='Имя актёра')

    class Meta():
        verbose_name='Актёр'
        verbose_name_plural='Актёры'

    def __str__(self):
        return self.full_name

class Release_Year(BaseModel):
    year = models.CharField(default='',max_length=4)

    class Meta():
        verbose_name='Год релиза'
        verbose_name_plural='Года релизов'

    def __str__(self):
        return self.year



class VideoProduct(BaseModel):
    image = models.ImageField(upload_to='images/pic', default="", verbose_name='Обложка')
    title = models.CharField(max_length=128, verbose_name='Оригинальное название фильма')
    directors = models.ManyToManyField(Director, verbose_name='Режиссёры')
    actors = models.ManyToManyField(Actor, verbose_name='Актёры')
    descriptions = models.TextField(max_length=1024, default="", verbose_name='Описание фильма')
    release_year = models.ForeignKey(
        Release_Year,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Дата выхода',)
    product_type = models.ManyToManyField(
        ProductType,
        verbose_name='Жанр'
    ) 
    original_title = models.OneToOneField(
        OriginalTitle, 
        on_delete=models.CASCADE,
        verbose_name='Выберите фильм'
    ) 

    class Meta():
        verbose_name='Фильм'
        verbose_name_plural='Фильмы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'original_title'),
                name='Ограничение на один фильм',
            ),
        )

    def __str__(self):
        return self.title

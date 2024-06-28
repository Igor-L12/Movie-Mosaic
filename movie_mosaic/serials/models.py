from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
    title = models.CharField(max_length=128, verbose_name='Название сериала')

    class Meta():
        verbose_name='Название сериала'
        verbose_name_plural='Название сериалов'

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

class SerialProduct(BaseModel):
    image = models.ImageField(upload_to='images/pic', default="", blank=True, verbose_name='Обложка')
    title = models.CharField(max_length=128, verbose_name='Оригинальное название сериала')
    directors = models.ManyToManyField(Director, verbose_name='Режиссёры')
    actors = models.ManyToManyField(Actor, verbose_name='Актёры')
    descriptions = models.TextField(max_length=1024, default="", verbose_name='Описание сериала')
    duration = models.IntegerField(default=0, verbose_name='Продолжительность серии')
    seasons = models.IntegerField(default=0, verbose_name='Кол-во сезонов')
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
        verbose_name='Название фильма в русской локализации',
        null=True,
        blank=True
    ) 

    moderated = models.BooleanField(default=False, verbose_name='Модерировано')
    
    class Meta():
        verbose_name='Сериал'
        verbose_name_plural='Сериалы'

    def __str__(self):
        return self.title



class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class RatingSerial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='serials_ratings')
    serial = models.ForeignKey(SerialProduct, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")

    def __str__(self):
        return f"{self.star} - {self.serial}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='serial_bookmarks')
    serial = models.ForeignKey(SerialProduct, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'serial')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные сериалы"

    def __str__(self):
        return f"{self.serial}. Пользователь: {self.user}"

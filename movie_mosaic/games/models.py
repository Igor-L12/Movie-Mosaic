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


class ProductType(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Жанр')

    class Meta():
        verbose_name='Жанр'
        verbose_name_plural='Жанры'

    def __str__(self):
        return self.title

class Director(BaseModel):
    full_name = models.CharField(max_length=128, verbose_name='Разработчик')

    class Meta():
        verbose_name='Разработчик'
        verbose_name_plural='Разработчики'

    def __str__(self):
        return self.full_name
    
class Release_Year(BaseModel):
    year = models.CharField(default='',max_length=4)

    class Meta():
        verbose_name='Год релиза'
        verbose_name_plural='Года релизов'

    def __str__(self):
        return self.year

class GameProduct(BaseModel):
    image = models.ImageField(upload_to='images/pic', default="", blank=True, verbose_name='Обложка')
    title = models.CharField(max_length=128, verbose_name='Название игры')
    directors = models.ManyToManyField(Director, verbose_name='Разработчик')
    descriptions = models.TextField(max_length=1024, default="", verbose_name='Описание игры')
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

    moderated = models.BooleanField(default=False, verbose_name='Модерировано')
    
    class Meta():
        verbose_name='Игра'
        verbose_name_plural='Игры'

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


class RatingGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_ratings')
    game = models.ForeignKey(GameProduct, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")

    def __str__(self):
        return f"{self.star} - {self.game}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_bookmarks')
    game = models.ForeignKey(GameProduct, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные игры"

    def __str__(self):
        return f"{self.game}. Пользователь: {self.user}"
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('nature', 'Природный объект'),
        ('historical', 'Историческое место'),
        ('recreation', 'Зона отдыха'),
        ('food', 'Еда / Ресторан'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="Категория")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='places', verbose_name="Создано пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @property
    def review_count(self):
        return self.reviews.count()

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews', verbose_name="Место")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Автор")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    text = models.TextField(max_length=1000, verbose_name="Текст отзыва")
    visit_date = models.DateField(verbose_name="Дата посещения")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Количество лайков")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        unique_together = ('place', 'author')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author.username} для {self.place.name}"

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', verbose_name="Изображение")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True, related_name='photos', verbose_name="Место")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True, related_name='photos', verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Фото {self.id}"

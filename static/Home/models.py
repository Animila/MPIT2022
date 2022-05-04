from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255)
    descr = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    data = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'news_slug': self.slug})

    class Meta:
        verbose_name = 'Новости'  # единственное число
        verbose_name_plural = 'Новости'  # множественное число
        ordering = ['-data', 'title']  # сортировка по имени и дате создания
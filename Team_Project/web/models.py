from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def game_list(self):
        return ','.join([i.name for i in self.game_set.all()])


class Game(models.Model):
    name = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    sku = models.IntegerField(default=0)
    game_type = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

    def category_list(self):
        return ','.join([i.name for i in self.game_type.all()])


class Video(models.Model):
    name = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255)

    def __str__(self):
        return self.name

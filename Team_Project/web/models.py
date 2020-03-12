from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def include_games(self):
        return ','.join([i.name for i in self.game_set.all()])


class Game(models.Model):
    name = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    appid = models.IntegerField(default=0)
    game_type = models.ManyToManyField(Category, blank=True, through='Tag')

    def __str__(self):
        return self.name

    def tags(self):
        return ','.join([i.name for i in self.game_type.all()])


class Tag(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'game_tag'


class Video(models.Model):
    name = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255)

    def __str__(self):
        return self.name

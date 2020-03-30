from django.contrib.auth.models import User
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
    appid = models.IntegerField(default=0)
    rawgid = models.IntegerField(default=0)
    game_type = models.ManyToManyField(Category,  null=True, blank=True, default=None, through='Tag')

    def __str__(self):
        return self.name

    def tags(self):
        return ','.join([i.name for i in self.game_type.all()])


class Tag(models.Model):
    game = models.ForeignKey(Game, null=True, blank=True, default=None, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        db_table = 'game_tag'


class Video(models.Model):
    name = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '---' + self.game.name


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, default=None, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '---' + self.game.name

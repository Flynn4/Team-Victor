from django.db import models

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    game_type = models.CharField(max_length=255)
    game_url = models.CharField(max_length=2083)

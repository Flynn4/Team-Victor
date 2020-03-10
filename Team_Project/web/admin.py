from django.contrib import admin
from .models import *


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_list']


admin.site.register(Game, GameAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_list']


admin.site.register(Category, CategoryAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'videoId']


admin.site.register(Video, VideoAdmin)
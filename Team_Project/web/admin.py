from django.contrib import admin
from .models import *


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'tags']


admin.site.register(Game, GameAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'include_games']



admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['game', 'category']

admin.site.register(Tag, TagAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'videoId']


admin.site.register(Video, VideoAdmin)

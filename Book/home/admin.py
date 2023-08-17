from django.contrib import admin
from .models import BookInfo
from django.contrib.admin.options import ModelAdmin

# Register your models here.


@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'title', 'pageCount', 'averageRating']



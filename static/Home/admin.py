from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'descr', 'image', 'data']
    list_display_links = ['pk', 'title']
    search_fields = ['title', 'descr']
    list_editable = ['image']
    list_filter = ['data']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(News, NewsAdmin)

from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('news/', news, name='news'),
    path('post/<slug:news_slug>', news_detail, name='news_detail'),
    path('vacation/<int:comp_code>/<slug:vac_id>', vacation_page, name='vac_page'),
    path('vacation/', vacation_list, name='vac_list'),

]
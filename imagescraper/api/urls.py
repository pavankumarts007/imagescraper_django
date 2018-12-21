from django.contrib import admin
from django.urls import path
from .views import CrawlerUrlsApi,ScrapedUrlsApi,ImageUrlsApi
urlpatterns = [
    path('sources/', CrawlerUrlsApi.as_view(), name='sources'),
    path('levels/', ScrapedUrlsApi.as_view(), name='levels'),
    path('images/', ImageUrlsApi.as_view(), name='images')
]
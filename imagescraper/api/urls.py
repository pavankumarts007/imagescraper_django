from django.contrib import admin
from django.urls import path
from .views import CrawlerUrlsApi,ScrapedUrlsApi,ImageUrlsApi,CrawlerUrlApi
urlpatterns = [
    path('sources/', CrawlerUrlsApi.as_view(), name='sources'),
    path('source/', CrawlerUrlApi.as_view(), name='source'),
    path('levels/', ScrapedUrlsApi.as_view(), name='levels'),
    path('images/', ImageUrlsApi.as_view(), name='images')
]
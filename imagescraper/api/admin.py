from django.contrib import admin
from .models import CrawlerUrls,ScrapedUrls,ImageUrls

admin.site.register(CrawlerUrls)
admin.site.register(ScrapedUrls)
admin.site.register(ImageUrls)
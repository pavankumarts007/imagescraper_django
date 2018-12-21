from rest_framework import serializers
from .models import CrawlerUrls,ScrapedUrls,ImageUrls
from django.utils import timezone

class CrawlerUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerUrls
        fields = ('__all__')
class ScrapedUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedUrls
        fields = ('__all__')
class ImageUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrls
        fields = ('__all__')
class ImageUrlsInfoSerializer(serializers.ModelSerializer):
    pageUrl = ScrapedUrlsSerializer( read_only=True)
    parentUrl = CrawlerUrlsSerializer( read_only=True)
    class Meta:
        model = CrawlerUrls
        fields = ('__all__')
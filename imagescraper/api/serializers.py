from rest_framework import serializers
from .models import CrawlerUrls,ScrapedUrls,ImageUrls
from django.utils import timezone
class CrawlerUrlsSerializer(serializers.ModelSerializer):
    def validate(self, data):
        url=data['url']
        if CrawlerUrls.objects.filter(url=url).exists():
            raise serializers.ValidationError("Url Already Exists")
        return data
    class Meta:
        model = CrawlerUrls
        fields = ('__all__')
class CrawlerUrlsExtendSerializer(serializers.ModelSerializer):
    image_count=serializers.SerializerMethodField('image_count_fn')
    links_count=serializers.SerializerMethodField('links_count_fn')
    def image_count_fn(self,obj):
        return ImageUrls.objects.filter(parentUrl=obj).count()
    def links_count_fn(self,obj):
        return ScrapedUrls.objects.filter(parentUrl=obj).count()
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
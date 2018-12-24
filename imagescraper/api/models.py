from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.utils import timezone
class CrawlerUrls(models.Model):
    title=models.CharField(max_length=50,null=True,blank=True)
    url=models.URLField(max_length=500,null=True,blank=True)
    depth=models.IntegerField(default=1)
    status=models.BooleanField(default=False)
    internalStatus=models.BooleanField(default=False)
    scraping=models.BooleanField(default=False)
    createdOn=models.DateTimeField(default=timezone.now)
    error=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.title if self.title else self.url
    class Meta:
        ordering = ['createdOn']
class ScrapedUrls(models.Model):
    title=models.CharField(max_length=50,null=True,blank=True)
    parentUrl=models.ForeignKey("CrawlerUrls", verbose_name="Website Url", on_delete=models.CASCADE)
    relatedUrl=models.ForeignKey("ScrapedUrls", null=True,blank=True,verbose_name="Related Url", on_delete=models.CASCADE)
    url=models.URLField(max_length=500,null=True,blank=True)
    depth=models.IntegerField(default=2)
    scraping=models.BooleanField(default=False)
    createdOn=models.DateTimeField(default=timezone.now)
    error=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.title if self.title else self.url
    class Meta:
        ordering = ['createdOn']   
class ImageUrls(models.Model):
    parentUrl=models.ForeignKey("CrawlerUrls", verbose_name="Website Url", on_delete=models.CASCADE)
    url=models.URLField(max_length=500,null=True,blank=True)
    pageUrl=models.ForeignKey("ScrapedUrls",null=True,blank=True, verbose_name="Image Page Url", on_delete=models.CASCADE)
    createdOn=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['createdOn']
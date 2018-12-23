from background_task import background
from scraper import Crawler
from .models import CrawlerUrls,ImageUrls,ScrapedUrls
from django.utils import timezone
@background(schedule=5)
def scrapeMainUrls():
    for url in CrawlerUrls.objects.filter(status=False):
        url.scraping=True
        url.save()
        try:
            c=Crawler(current_page=url.url)
            c.open()
            if c.getImages():
                for image in c.getImages():
                    if image.startswith(url.url) and not ImageUrls.objects.filter(url=image).exists():
                        ImageUrls.objects.create(url=image,parentUrl=url.url,pageUrl=url.url,createdOn=timezone.now)
            if c.getPageLinks():
                for link in c.getPageLinks():
                    if link.startswith(url.url) and not ScrapedUrls.objects.filter(url=link).exists():
                        ScrapedUrls.objects.create(url=link,parentUrl=url.url,relatedUrl=url.url,createdOn=timezone.now,depth=2)
            url.scraping=False
            url.status=True
            url.internalStatus=True if url.depth == 1 else False
            url.save()
        except Exception as ex:
            print(ex)      
            url.error="unable Extract Images and Links from {0}".format(url.url)
            url.scraping=False
            url.save()

@background(schedule=5)
def scrapeInternalUrls():
    for url in CrawlerUrls.objects.filter(status=True,internalStatus=False):
        try:
            c=Crawler(current_page=url.url)
            c.open()
            if c.getImages():
                for image in c.getImages():
                    if image.startswith(url.url) and not ImageUrls.objects.filter(url=image).exists():
                        ImageUrls.objects.create(url=image,parentUrl=url.url,pageUrl=url.url,createdOn=timezone.now)
            if c.getPageLinks():
                for link in c.getPageLinks():
                    if link.startswith(url.url) and not ScrapedUrls.objects.filter(url=link).exists():
                        ScrapedUrls.objects.create(url=link,parentUrl=url.url,relatedUrl=url.url,createdOn=timezone.now,depth=2)
        except Exception as ex:
            print(ex)      
            url.error="unable Extract Images and Links from {0}".format(url.url)
            url.save()

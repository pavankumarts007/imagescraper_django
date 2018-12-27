from background_task import background
from .scraper import Crawler
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
                        ImageUrls.objects.create(url=image,parentUrl=url,pageUrl=None,createdOn=timezone.now())
            if c.getPageLinks():
                for link in c.getPageLinks():
                    if link.startswith(url.url) and not ScrapedUrls.objects.filter(url=link).exists():
                        ScrapedUrls.objects.create(url=link,parentUrl=url,relatedUrl=None,createdOn=timezone.now(),depth=2)
            if url.depth > 1:
                scrapeInternalUrls(id=url.id)
                url.internalStatus=False
            else:
                url.internalStatus=True

            url.scraping=False
            url.status=True
            url.save()

        except Exception as ex:
            raise
            print(ex)      
            url.error="unable Extract Images and Links from {0}".format(url.url)
            url.scraping=False
            url.save()

@background(schedule=5)
def scrapeInternalUrls(id=None):
    parent=CrawlerUrls.objects.get(id=id)
    for url in ScrapedUrls.objects.filter(parentUrl=parent):
        try:
            c=Crawler(current_page=url.url)
            c.open()
            if c.getImages():
                for image in c.getImages():
                    if image.startswith(parent.url) and not ImageUrls.objects.filter(url=image).exists():
                        ImageUrls.objects.create(url=image,parentUrl=parent,pageUrl=url,createdOn=timezone.now())
            if c.getPageLinks():
                for link in c.getPageLinks():
                    if link.startswith(parent.url) and not ScrapedUrls.objects.filter(url=link).exists():
                        ScrapedUrls.objects.create(url=link,parentUrl=parent,relatedUrl=url,createdOn=timezone.now(),depth=url.depth+1)
            if parent.depth > url.depth:
                scrapeSubInternalUrls(id=url.id)
        except Exception as ex:
            raise
            print(ex)      
            url.error="unable Extract Images and Links from {0}".format(url.url)
            url.save()
    if parent.depth==2:
        parent.internalStatus=True
        parent.save()

@background(schedule=5)
def scrapeSubInternalUrls(id=None):
    parent=ScrapedUrls.objects.get(id=id)
    suburls=ScrapedUrls.objects.filter(relatedUrl=parent)
    for url in suburls:
        try:
            c=Crawler(current_page=url.url)
            c.open()
            if c.getImages():
                for image in c.getImages():
                    if image.startswith(parent.url) and not ImageUrls.objects.filter(url=image).exists():
                        ImageUrls.objects.create(url=image,parentUrl=parent.parentUrl,pageUrl=url,createdOn=timezone.now())
            if c.getPageLinks():
                for link in c.getPageLinks():
                    if link.startswith(parent.url) and not ScrapedUrls.objects.filter(url=link).exists():
                        ScrapedUrls.objects.create(url=link,parentUrl=parent.parentUrl,relatedUrl=url,createdOn=timezone.now(),depth=url.depth+1)
            if parent.parentUrl.depth > url.depth+1:
                scrapeSubInternalUrls(id=url.id)
        except Exception as ex:
            raise
            print(ex)      
            url.error="unable Extract Images and Links from {0}".format(url.url)
            url.save()
    if parent.parentUrl.depth==parent.depth+1:
        parent.parentUrl.internalStatus=True
        parent.parentUrl.save()
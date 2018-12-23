from background_task import background
from scraper import Crawler
from .models import CrawlerUrls,ImageUrls,ScrapedUrls
from django.utils import timezone
@background(schedule=5)
def scrape():
    for url in CrawlerUrls.objects.filter(status=False):
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

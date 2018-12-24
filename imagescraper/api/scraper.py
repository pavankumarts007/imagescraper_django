from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


class Crawler(object):

    def __init__(self,current_page=None):
        self.soup = None
        self.current_page   = current_page
        self.images  = []
        self.page_links=[]
    def getImages(self):
        return self.images
    def getPageLinks(self):
        return self.page_links
    def open(self):
        print(self.current_page)
        res = requests.get(self.current_page)
        if res.status_code == 200:
            html_code = res.text
        
            self.soup = BeautifulSoup(html_code,features="html.parser")

            try :
                for link in [h.get('href') for h in self.soup.find_all('a')]:
                    print("Found link: '" + link + "'")
                    if link.startswith('http'):
                        self.page_links.append(link)
                        print("Adding link" + link + "\n")
                    elif link.startswith('/'):
                        parts = urlparse(self.current_page)
                        self.page_links.append(parts.scheme + '://' + parts.netloc + link)
                        print("Adding link " + parts.scheme + '://' + parts.netloc + link + "\n")
                    else:
                        if not link.startswith("#"):
                            self.page_links.append(self.current_page+link)
                            print("Adding link " + self.current_page+link + "\n")

            except Exception as ex:
                print(ex)
            try :
                for link in [h.get('src') for h in self.soup.find_all('img')]:
                    print("Found link: '" + link + "'")
                    if link.startswith('http'):
                        self.images.append(link)
                        print("Adding link" + link + "\n")
                    elif link.startswith('/'):
                        parts = urlparse(self.current_page)
                        self.images.append(parts.scheme + '://' + parts.netloc + link)
                        print("Adding link " + parts.scheme + '://' + parts.netloc + link + "\n")
                    else:
                        self.images.append(self.current_page+link)
                        print("Adding link " + self.current_page+link + "\n")

            except Exception as ex:
                print(ex)
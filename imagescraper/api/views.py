from django.shortcuts import render
#rest imports
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
#in app imports
from .models import CrawlerUrls,ScrapedUrls,ImageUrls
from .serializers import CrawlerUrlsSerializer,ScrapedUrlsSerializer,ImageUrlsSerializer,ImageUrlsInfoSerializer,CrawlerUrlsExtendSerializer

class CrawlerUrlApi(APIView):
    renderer_classes = [JSONRenderer]
    def post(self,request):
        serializer=CrawlerUrlsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer=CrawlerUrlsExtendSerializer(CrawlerUrls.objects.get(id=serializer.data.get('id')))
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        id=request.GET.get('id','')
        try:
            CrawlerUrls.objects.get(id=id).delete()
        except:
            return Response({'error':{'non_field_errors':['Not Found']}},status=status.HTTP_404_NOT_FOUND)
        return Response({},status=status.HTTP_201_CREATED)
class CrawlerUrlsApi(generics.ListAPIView):
    serializer_class=CrawlerUrlsExtendSerializer
    renderer_classes = [JSONRenderer]
    def get_queryset(self):
        urls = CrawlerUrls.objects.all()
        if "id" in self.request.query_params:
            id = self.request.query_params.get('id')
            urls = urls.filter(id=id)
        if "status" in self.request.query_params:
            status = self.request.query_params.get('status')
            urls = urls.filter(status=True if status == "true" else False)
        return urls
class ScrapedUrlsApi(generics.ListAPIView):
    serializer_class=ScrapedUrlsSerializer
    renderer_classes = [JSONRenderer]
    def get_queryset(self):
        urls = ScrapedUrls.objects.all()
        if "id" in self.request.query_params:
            id = self.request.query_params.get('id')
            urls = urls.filter(id=id)
        if "parent" in self.request.query_params:
            parent = self.request.query_params.get('parent')
            urls = urls.filter(parentUrl__id=parent)
        if "related" in self.request.query_params:
            related = self.request.query_params.get('related')
            urls = urls.filter(relatedUrl__id=related)
        if "depth" in self.request.query_params:
            depth = self.request.query_params.get('depth')
            urls = urls.filter(depth=depth)
        return urls
class ImageUrlsApi(generics.ListAPIView):
    serializer_class=ImageUrlsSerializer
    renderer_classes = [JSONRenderer]
    def get_queryset(self):
        urls = ImageUrls.objects.all()
        if "id" in self.request.query_params:
            id = self.request.query_params.get('id')
            urls = urls.filter(id=id)
        if "parent" in self.request.query_params:
            parent = self.request.query_params.get('parent')
            urls = urls.filter(parentUrl__id=parent)
        if "related" in self.request.query_params:
            related = self.request.query_params.get('related')
            urls = urls.filter(pageUrl__id=related)
        return urls
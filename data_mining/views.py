from django.http import HttpResponse
from django.shortcuts import render
from data_mining.core.crawler import Crawler
from data_mining.models import crawler_config, video
from rest_framework.views import APIView
from data_mining.serializers import crawler_config_serializer,video_serializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import viewsets
# Create your views here.
from rest_framework.decorators import action

def startXnxx(request):
    # crawler = Crawler()
    # crawler.get_page()
    # crawler.close()
    return HttpResponse("访问结束")


class CrawlerConfigViewSet(viewsets.ModelViewSet):

    """
        retrieve:
            返回指定爬虫配置信息

        list:
            返回爬虫配置集合

        create:
            创建一个新的爬虫配置

        delete:
            移除一个已经存在的爬虫配置

        partial_update:
            更新爬虫配置的一个或多个字段

        update:
            更新爬虫配置
    """
    queryset = crawler_config.CrawlerConfig.objects.all()
    serializer_class = crawler_config_serializer.CrawlerConfigSerializer


class VideoViewSet(viewsets.ModelViewSet):

    """
        retrieve:
            返回指定视频信息

        list:
            返回视频集合

        create:
            创建一个新的视频

        delete:
            移除一个已经存在的视频

        partial_update:
            更新视频信息的一个或多个字段

        update:
            更新视频信息
    """

    queryset = video.Video.objects.all()
    serializer_class = video_serializer.VideoSerializer

    # @action(detail=True, methods='get')
    # def download_video(self, request, *args, **kwargs):
    #
    #     return Response('1')
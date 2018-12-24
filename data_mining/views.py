from django.http import HttpResponse
from django.shortcuts import render
from data_mining.core.crawler import Crawler
# Create your views here.

def startXnxx(request):
    crawler = Crawler()
    crawler.get_page()
    crawler.close()
    return HttpResponse("访问结束")
from django.db import models
from . import common


class CrawlerConfig(common.Common):
    site = models.CharField("目标首页", unique=True, max_length=1000)
    data_url = models.CharField("数据采集网址", unique=True, max_length=1000)
    is_running = models.IntegerField("是否在运行", default=0)
    site_type = models.IntegerField("网站类型: 0视频网站,1小说网站2新闻网站3图片网站",default=0)

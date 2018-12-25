from django.db import models
from . import crawler_config

class Video(models.Model):
    crawler_config = models.ForeignKey(crawler_config.CrawlerConfig, on_delete=models.CASCADE)
    # 视频标题
    video_title = models.CharField("视频标题",max_length=500)
    # 视频预览图片存放地址
    video_preview_url = models.CharField("视频预览图片存放地址",max_length=500)
    # 视频点击数
    video_hits = models.CharField("视频点击数",max_length=50)
    # 视频长度
    video_length = models.CharField("视频长度",max_length=50)
    # 视频原始Id
    video_original_id = models.CharField("视频原始Id",max_length=10)
    # 视频原始URL
    video_original__url = models.CharField("视频原始URL",max_length=500)
    # 视频现存地址
    video_new_url = models.CharField("视频现存地址",max_length=500)
    # 视频网站URL
    video_site_url = models.CharField("视频网站URL",max_length=500)
    # 视频是否已被下载
    video_active = models.IntegerField(default=0)
    # 视频原始地址是否有效
    video_original__url_disable = models.IntegerField(default=0)



    def __str__(self):
        return self.video_title
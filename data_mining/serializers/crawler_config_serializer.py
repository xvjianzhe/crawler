from rest_framework import serializers
from data_mining.models import crawler_config


class CrawlerConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = crawler_config.CrawlerConfig
        fields = "__all__"

from rest_framework import serializers
from data_mining.models import video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = video.Video
        fields = "__all__"


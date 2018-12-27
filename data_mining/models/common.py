from django.db import models
from django.utils import timezone


class Common(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    disable = models.IntegerField(default=0)

    class Meta:
        abstract=True

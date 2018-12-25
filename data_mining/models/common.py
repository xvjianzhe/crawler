from django.db import models


class Common(models.Model):
    create_time = models.DateTimeField(auto_created=True)
    update_time = models.DateTimeField(auto_now_add=True)
    disable = models.IntegerField(default=0)

    class Meta:
        abstract=True

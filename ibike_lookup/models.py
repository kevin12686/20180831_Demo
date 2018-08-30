from django.db import models


# Create your models here.

class station(models.Model):
    area = models.CharField(max_length=10, verbose_name='區域')
    location = models.CharField(max_length=20, verbose_name='租賃點')
    bikes = models.IntegerField(verbose_name='可借車輛')
    spaces = models.IntegerField(verbose_name='可停空位')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='最後更新時間')

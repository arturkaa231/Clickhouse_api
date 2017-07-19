from django.db import models
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime,date
# Create your models here.
class Data(models.Model):
    class Meta():
        db_table='Data'
    Data_size=models.IntegerField(default=0)
    Data_win=models.IntegerField(default=0)
    Data_minc=models.IntegerField(default=0)
    Data_xls=models.FileField(blank=True, null=True, default=None)
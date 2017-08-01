from django.db import models
from django.db import models
from django.core.urlresolvers import reverse
from uuid import uuid4
import os.path



# Create your models here.
class Data(models.Model):
    class Meta():
        db_table='Data'

    Data_title=models.CharField(default=None,blank=True, null=True,max_length=100, )
    Data_xls = models.FileField(blank=True, null=True,default=None)

    def get_text(self):
        return self.tags_set.all()
    def __unicode__(self):
        return self.Data_title



class Tags(models.Model):
    class Meta():
        db_table='tags'
    tg=models.CharField(max_length=100,default=None,blank=True, null=True)
    text=models.ForeignKey(Data,null=True, blank=True,related_name='TAGS')
class Options(models.Model):
    class Meta():
        db_table = 'Options'


    size = models.IntegerField()
    win = models.IntegerField()
    minc = models.IntegerField()

    img=models.ImageField(blank=True, null=True, default=None)
    text=models.ForeignKey(Data,null=True, blank=True)
    script=models.TextField(blank=True, null=True, default=None)
    div = models.TextField(blank=True, null=True, default=None)

class Templates(models.Model):
    class Meta():
        db_table='Temp'

    size = models.IntegerField(default=300)
    win = models.IntegerField(default=5)
    minc = models.IntegerField(default=30)



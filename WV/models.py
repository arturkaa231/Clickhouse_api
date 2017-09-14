from django.db import models
from django.db import models
from django.core.urlresolvers import reverse
from uuid import uuid4
import os.path
from django.db.models.signals import post_delete
from django.core.files.storage import FileSystemStorage
from Word2Vec.settings import STATIC_ROOT
fs = FileSystemStorage(location='/opt/static/')
# Create your models here.
class Data(models.Model):
    class Meta():
        db_table='Data'

    Data_title=models.CharField(default=None,blank=True, null=True,max_length=100, )
    Data_xls = models.FileField(blank=True, null=True,default=None)
    Data_model=models.FileField(blank=True,null=True,default=None)
    def get_text(self):
        return self.tags_set.all()
    def __unicode__(self):
        return self.Data_title
class Tags(models.Model):
    class Meta():
        db_table='tags'
    tg=models.CharField(max_length=100,default=None,blank=True, null=True)
    text=models.ForeignKey(Data,null=True, blank=True,related_name='TAGS',on_delete=models.SET_NULL)
class Options(models.Model):
    class Meta():
        db_table = 'Options'
    size = models.IntegerField()
    win = models.IntegerField()
    minc = models.IntegerField()
    cbow=models.BooleanField(blank=True,default=False)
    skipgr = models.BooleanField(blank=True, default=True)
    alg=models.IntegerField(blank=True, null=True, default=0)
    text=models.ForeignKey(Data,null=True, blank=True, on_delete=models.SET_NULL)
    preview=models.ImageField(blank=True, null=True, default=None, storage=fs)
class ImageOptions(models.Model):
    class Meta():
        db_table = 'Images'

    num_clusters = models.IntegerField(default=20)
    img = models.ImageField(blank=True, null=True, default=None, storage=fs)
    script = models.TextField(blank=True, null=True, default=None)
    div = models.TextField(blank=True, null=True, default=None)
    num_neighbors=models.IntegerField(default=30,null=True,blank=True)
    opt = models.ForeignKey(Options, null=True, blank=True,related_name='image', on_delete=models.SET_NULL)
class Templates(models.Model):
    class Meta():
        db_table='Temp'

    size = models.IntegerField(default=300)
    win = models.IntegerField(default=5)
    minc = models.IntegerField(default=30)

def delete_Data_Data_xls(sender, **kwargs):
    """
    Процедура, ловящая сигнал при удалении записи,
    и производящая собственно удаление файла
    """
    mf = kwargs.get("instance")
    mf.Data_xls.delete(save=False)
    mf.Data_model.delete(save=False)
def delete_ImageOptions_img(sender, **kwargs):
    """
    Процедура, ловящая сигнал при удалении записи,
    и производящая собственно удаление файла
    """

    mf = kwargs.get("instance")
    storage=mf.img.storage
    storage.delete(mf.img)

# Теперь зарегистрируем нашу функцию для удаления
post_delete.connect(delete_Data_Data_xls, Data)

# Теперь зарегистрируем нашу функцию для удаления
post_delete.connect(delete_ImageOptions_img, ImageOptions)

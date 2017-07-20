from django.db import models
from django.db import models
from django.core.urlresolvers import reverse
from uuid import uuid4
import os.path

# Create your models here.
class Data(models.Model):
    class Meta():
        db_table='Data'

    def path_and_rename(path):
        def wrapper(instance, filename):
            ext = filename.split('.')[-1]
            # get filename
            filename = '{}.{}'.format(uuid4().hex, ext)
            # return the whole path to the file

            return os.path.join(path, filename)

        return wrapper
    print(path_and_rename('Excel'))
    Data_size=models.IntegerField(default=300)
    Data_win=models.IntegerField(default=5)
    Data_minc=models.IntegerField(default=30)
    Data_xls=models.FileField(blank=True, null=True, default=None)





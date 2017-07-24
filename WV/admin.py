from django.contrib import admin

from WV.models import Templates,Data

class DataAdmin(admin.ModelAdmin):
   fields = ['Data_size','Data_minc','Data_win','Data_title','Data_xls']


admin.site.register(Data,DataAdmin)
# Register your models here.

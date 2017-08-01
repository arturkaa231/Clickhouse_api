from django.contrib import admin

from WV.models import Templates,Data,Tags,Options

class DataAdmin(admin.ModelAdmin):
    fields = ['Data_title','Data_xls']
class TemplatesAdmin(admin.ModelAdmin):
    fields = ['size', 'minc', 'win']
class DataInLine(admin.StackedInline):
    model=Tags
    extra=2
class DataInLine2(admin.StackedInline):
    model=Options
    extra=2


admin.site.register(Data,DataAdmin)
admin.site.register(Templates,TemplatesAdmin)
# Register your models here.

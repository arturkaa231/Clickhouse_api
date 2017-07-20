from django.forms import ModelForm, fields,forms
from WV.models import Data
from Word2Vec import settings
from django.template.defaultfilters import filesizeformat
class EnterData(ModelForm):
    class Meta:
        model=Data
        fields = ['Data_minc','Data_size','Data_win','Data_xls']

    def __str__(self):
        return self.as_div()

  
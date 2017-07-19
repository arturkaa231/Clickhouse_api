from django.forms import ModelForm, fields,forms
from WV.models import Data

class EnterData(ModelForm):
    class Meta:
        model=Data
        fields = ['Data_minc','Data_size','Data_win','Data_xls']

    def __str__(self):
        return self.as_div()
from django.forms import ModelForm, fields,forms
from WV.models import Data,Options
from Word2Vec import settings
from uuid import uuid4
import os.path
class EnterOptions(ModelForm):
    class Meta:
        model = Options
        fields = ['size','win','minc']

    def __str__(self):
        return self.as_div()



class EnterData(ModelForm):

    class Meta:
        model=Data
        fields = ['Data_title','Data_xls',]

    def __str__(self):
        return self.as_div()

    def clean(self):
        def ChangeName(filename):
            ext = filename.split('.')[-1]
            # get filename
            filename = '{}.{}'.format(uuid4().hex, ext)
            # return the whole path to the file
            return filename
        cleaned_data = self.cleaned_data
        cleaned_data['Data_xls'].name=ChangeName(filename= cleaned_data['Data_xls'].name)
        print(cleaned_data)

        return cleaned_data
    def is_valid(self):

        valid = super(EnterData, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid
        extensions = ['.xls', '.xlsx','.xlsm','.csv','.xlt','.xltx' ]

        filename, file_extension = os.path.splitext(self.cleaned_data['Data_xls'].name)
        if file_extension not in extensions:

            return False
        # run the parent validation first
        else:
            return True



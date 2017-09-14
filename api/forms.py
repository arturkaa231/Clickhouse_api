from django.forms import ModelForm,fields
from django import forms
class RequestForm(forms.Form):
    structure=forms.CharField()
    order_by=forms.CharField()
    sort_order=forms.CharField()
    nb_visits=forms.IntegerField()
    nb_actions=forms.IntegerField()
    limit=forms.IntegerField()
    offset=forms.IntegerField()
    dimensions=forms.CharField()
    date1=forms.DateField()
    date2=forms.DateField()
    filt=forms.CharField()


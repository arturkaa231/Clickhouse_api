from django.conf.urls import url
from spyrecorder import views

urlpatterns = [
    url(r'^',views.AddCH, name='AddCH'),



]


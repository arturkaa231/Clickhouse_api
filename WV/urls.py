from django.conf.urls import url
from WV import views

urlpatterns = [

    url(r'^',views.mainPage, name='EnterData'),


]

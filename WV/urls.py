from django.conf.urls import url
from WV import views

urlpatterns = [
    url(r'^DownloadedTexts/(?P<page_number>\d+)/$',views.DownloadedTexts, name='DownloadedTexts'),
    url(r'^showmap/(?P<Opt_id>\d+)/$',views.showmap, name='showmap'),
    url(r'^maps/(?P<Data_id>\d+)/(?P<page_number>\d+)/$',views.maps, name='maps'),
    url(r'^template/(?P<size>\d+)/(?P<win>\d+)/(?P<minc>\d+)/(?P<Data_id>\d+)/$', views.template, name='template'),
    url(r'^options/(?P<Data_id>\d+)/$', views.enteroptions, name='options'),

    url(r'^',views.mainPage, name='EnterData'),



]

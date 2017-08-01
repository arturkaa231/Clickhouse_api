from django.conf.urls import url
from WV import views

urlpatterns = [
    url(r'^downloadedtexts/(?P<page_number>\d+)/$',views.DownloadedTexts, name='DownloadedTexts'),
    url(r'^filteredtexts/(?P<page_number>\d+)/(?P<tags>\w+)/$',views.FilteredTexts, name='FilteredTexts'),
    url(r'^showmap/(?P<Opt_id>\d+)/(?P<Data_id>\d+)/$',views.Showmap, name='showmap'),
    url(r'^maps/(?P<Data_id>\d+)/(?P<page_number>\d+)/$',views.Maps, name='maps'),
    url(r'^template/(?P<size>\d+)/(?P<win>\d+)/(?P<minc>\d+)/(?P<Data_id>\d+)/$', views.Template, name='template'),
    url(r'^options/(?P<Data_id>\d+)/$', views.Enteroptions, name='options'),

    url(r'^',views.MainPage, name='EnterData'),



]

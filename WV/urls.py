from django.conf.urls import url
from WV import views

urlpatterns = [
    url(r'^downloadedtexts/(?P<page_number>\d+)/$',views.DownloadedTexts, name='DownloadedTexts'),
    url(r'^filteredtexts/(?P<page_number>\d+)/(?P<tags>\S+)/$',views.FilteredTexts, name='FilteredTexts'),
    url(r'^showmap/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<Img_id>\d+)/$',views.Showmap, name='showmap'),
    url(r'^maps/(?P<Data_id>\d+)/(?P<page_number>\d+)/$',views.Maps, name='maps'),
    url(r'^images/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<page_number>\d+)/$', views.Images, name='images'),
    url(r'^deleteopt/(?P<Opt_id>\d+)/(?P<Data_id>\d+)/$',views.DeleteOpt, name='deleteopt'),
    url(r'^deleteimg/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<Img_id>\d+)/$',views.DeleteImageOpt, name='deleteimg'),
    url(r'^template/(?P<size>\d+)/(?P<win>\d+)/(?P<minc>\d+)/(?P<Data_id>\d+)/$', views.Template, name='template'),
    url(r'^options/(?P<Data_id>\d+)/$', views.Enteroptions, name='options'),
    url(r'^imageoptions/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/$', views.EnterImageOptions, name='imageoptions'),
    url(r'^setpreview/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<img>\S+)/$', views.SetPreview, name='setpreview'),
    url(r'^centroids/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<Img_id>\d+)/$', views.Centroids, name='centroids'),
    url(r'^minfreq/(?P<Data_id>\d+)/(?P<Opt_id>\d+)/(?P<Img_id>\d+)/$', views.MinFrequencyWord, name='minfreq'),
    url(r'^similarwords/$', views.SimilarWords, name='similarwords'),
    url(r'^downloadtext/(?P<Data_id>\d+)/$',views.DownloadText, name='downloadtext'),
    url(r'^',views.MainPage, name='EnterData'),



]


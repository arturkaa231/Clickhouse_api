from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.paginator import Paginator
from datetime import datetime,date
from gensim.models import Word2Vec
import xlrd
import xlwt
import os.path
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label,Tool
from bokeh.models import CustomJS,TapTool,LassoSelectTool
from bokeh.models.widgets import TextInput
import random
from WV.models import Data,Templates,Options,Tags
from WV.forms import EnterData,EnterOptions,TagsForm
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
from Word2Vec.settings import BASE_DIR,MEDIA_ROOT,STATICFILES_DIRS
from uuid import uuid4
from bokeh.io import export_png,export_svgs
from bokeh.models.sources import AjaxDataSource
from django.http import JsonResponse


def MainPage(request):
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username

    if request.method=="POST":
        form_text=EnterData(request.POST, request.FILES)
        form_tg=TagsForm(request.POST)
        #form.article_auth=auth.get_user(request).username

        if  form_text.is_valid() and form_tg.is_valid():
            form_text.save()
            #разделяем строку с тегами на отдельные теги
            def Split(tags):
                return tags.split(',')
            cleaned_tags=Split(request.POST['tg'])

            for i in cleaned_tags:
                tg=Tags(text_id=Data.objects.get(Data_xls=request.FILES['Data_xls']).id,tg=i)
                tg.save()
            return redirect(reverse('options',args=[Data.objects.get(Data_xls=request.FILES['Data_xls']).id]))

        else:
            args['form_text'] = EnterData
            args['form'] = TagsForm
            args['error'] = 'The file is not supported. Or bad tags'
            return render_to_response('EnterData.html', args)
    else:
        args['form_text'] = EnterData
        args['form'] = TagsForm
        return render_to_response('EnterData.html', args)

def Enteroptions(request,Data_id):
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username

    if request.method == "POST":
        form = EnterOptions(request.POST)
        data=Data.objects.get(id=Data_id)
        xls=data.Data_xls

        if form.is_valid():
            options=form.save(commit=False)
            options.text=Data.objects.get(Data_xls=xls)
            #проверка на повторяющиеся сеты параметров
            for i in Options.objects.filter(text_id=Data_id)[:]:
                if int(request.POST['size'])==i.size and int(request.POST['win'])== i.win and int(request.POST['minc'])== i.minc:
                    args = {}
                    args.update(csrf(request))
                    args['username'] = auth.get_user(request).username
                    args['form'] = EnterOptions
                    args['templates'] = Templates.objects.all()
                    args['Data_id'] = Data_id
                    args['error'] = 'these parameters already exist'
                    return render_to_response('EnterOptions.html', args)

            def Map(xls, size, win, minc):
                def clean(text):
                    for i in ['/',";","'",'.',',','#', ':', '!', '?','%','^','<','>','&',')','(','{','}',']','[','$','@']:
                        text = text.replace(i, '')

                    return text

                # Read words from  xls
                def ReadXls(xls):
                    wb = xlrd.open_workbook(os.path.join(xls))
                    wb.sheet_names()
                    sh = wb.sheet_by_index(0)
                    WL = []
                    i = 0
                    while i < sh.nrows:
                        Load = sh.cell(i, 0).value
                        WL.append(Load)
                        i += 1
                    return WL

                # Write to xls
                def WriteXls(xls):
                    # rb=xlrd.open_workbook(a)
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('result')
                    # sheet=book.sheet_by_index(0)
                    # wb=xlcopy(rb)

                    ws = wb.get_sheet(0)
                    k = 0

                    for i in model.wv.vocab.keys():
                        ws.write(k, 0, i)

                        k += 1
                    k = 0

                    for i in model.wv.vocab.keys():
                        ws.write(k, 1, str(model.wv[i]))

                        k += 1
                    wb.save(xls)

                def BuildWordMap():
                    h = .02  # step size in the mesh
                    for weights in ['uniform', 'distance']:
                        # we create an instance of Neighbours Classifier and fit the data.

                        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
                        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
                        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                                             np.arange(y_min, y_max, h))

                        plt.xlim(-1, 1)
                        plt.ylim(-1, 1)
                        plt.title('words map')

                    for i, text in enumerate(model.wv.vocab.keys()):
                        plt.annotate(text, (X[:, 0][i], X[:, 1][i]))

                    plt.show()

                def BuildHtmlMap():


                    s1 = ColumnDataSource(data=dict(x=list(X[:, 0]), y=list(X[:, 1]), words=list(model.wv.vocab.keys()),
                                                    color=['#000000' for i in range(len(list(model.wv.vocab.keys())))]))#data_url='http://localhost:8000/view2d/data/',polling_interval=100,method='GET')
                    p1 = figure(tools="pan,lasso_select,wheel_zoom,reset,save,tap", title="Word map",
                                plot_width=1500, plot_height=900, x_range=Range1d(-0.1, 0.1))

                    p1.scatter(x='x', y='y', size=10, source=s1, alpha=0, color='#000000')
                    labels = LabelSet(x='x', y='y', text_color='color', text='words',
                                      x_offset=-7, y_offset=-7, source=s1, render_mode='canvas')

                    citation = Label(x=70, y=70, x_units='screen', y_units='screen',
                                     text='', render_mode='css',
                                     border_line_color='black', border_line_alpha=10.0,
                                     background_fill_color='white', background_fill_alpha=1.0, )

                    s1.callback = CustomJS(args=dict(s1=s1), code="""
                                                                         var inds = cb_obj.selected['1d'].indices;
                                                                         var d1 = cb_obj.data;
                                                                         for (i = 0; i < inds.length; i++) {
                                                                            d1['color'][inds[i]]='#DC143C'

                                                                         }
                                                                         s1.change.emit();
                                                                     """)

                    tap = p1.select(type=TapTool)
                    tap.callback = CustomJS(args=dict(s1=s1), code="""
                                                          var inds = cb_obj.selected['1d'].indices;
                                                          var d1 = cb_obj.data;
                                                          for (i = 0; i < inds.length; i++) {
                                                              d1['words'][inds[i]]=''
                                                              d1['x'][inds[i]]=100


                                                          }
                                                          s1.change.emit();
                                                      """)


                    p1.add_layout(labels)
                    p1.add_layout(citation)

                    script, div = components(p1)
                    def ChangeName(filename):
                        ext = filename.split('.')[-1]
                        # get filename
                        filename = '{}.{}'.format(uuid4().hex, ext)
                        # return the whole path to the file
                        return filename
                    picture_name=ChangeName('.png')

                    export_png(p1,os.path.join(STATICFILES_DIRS[1],picture_name))
                    options.img=picture_name
                    options.script=script
                    options.div=div
                    form.save()
                    args['username'] = auth.get_user(request).username
                    args['script'] = script
                    args['div'] = div
                    args['Data_id']=Data_id

                WL = ReadXls(xls)
                W = []
                # clean from punctuations
                for i in WL:
                    i = clean(i)
                    W.append(i)
                Words = []
                for i in W:
                    i = i.split(' ')
                    Words.append(i)

                # Create the model
                model = Word2Vec(Words, size=size, window=win, min_count=minc)

                X = []
                for i in model.wv.vocab.keys():
                    X.append(model.wv[i])
                X = np.array(X)

                #WriteXls(xls)
                # BuildWordMap()
                BuildHtmlMap()
                return args
        #переделать на ajax
            return render_to_response('WordMap.html', Map(os.path.join(MEDIA_ROOT,str(xls)),
                                                          int(request.POST['size']), int(request.POST['win']),
                                                          int(request.POST['minc'])))
    else:
        args['form'] = EnterOptions
        args['templates']=Templates.objects.all()
        args['Data_id']=Data_id
        return render_to_response('EnterOptions.html',args)


#вывод шаблонов
def Template(request,size,win,minc,Data_id):
    args={}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    args['form'] = EnterOptions
    args['templates'] = Templates.objects.all()
    args['size']=size
    args['win'] = win
    args['minc'] = minc
    args['Data_id']=Data_id
    return render_to_response('EnterOptions.html', args)

def DownloadedTexts(request,page_number=1):
    args={}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    # Добавление пагинации


    if request.method=="POST" :
        form=TagsForm(request.POST)
        if form.is_valid():
            #теги совпадающие с введеным в фильтр тегов
            return redirect(reverse('FilteredTexts',args=[1,request.POST['tg']]))
        else:
            all_texts = Data.objects.all().order_by('-id')
            args['texts'] = Paginator(all_texts, 10).page(page_number)
            args['form'] = TagsForm
            return render_to_response('DownloadedTexts.html', args)
    else:
        all_texts = Data.objects.all().order_by('-id')
        args['texts'] = Paginator(all_texts, 10).page(page_number)
        args['form']=TagsForm
        return render_to_response('DownloadedTexts.html',args)

def FilteredTexts(request, page_number=1,tags=''):
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    # Добавление пагинации


    if request.method == "POST":
        form = TagsForm(request.POST)
        if form.is_valid():
            # теги совпадающие с введеным в фильтр тегом
            return redirect(reverse('FilteredTexts',args=[1,request.POST['tg']]))
        else:
            tgs = Tags.objects.filter(tg=tags)
            all_texts = []
            for i in tgs:
                all_texts.append(Data.objects.get(id=i.text_id))

            args['tags'] = tags
            args['texts'] = Paginator(all_texts, 10).page(page_number)
            args['form'] = TagsForm
            return render_to_response('FilteredTexts.html', args)
    else:

        tgs = Tags.objects.filter(tg=tags)
        all_texts = []
        for i in tgs:
            all_texts.append(Data.objects.get(id=i.text_id))

        args['tags'] = tags
        args['texts'] = Paginator(all_texts, 10).page(page_number)
        args['form'] = TagsForm
        return render_to_response('FilteredTexts.html', args)
def Maps(request,Data_id,page_number=1):
    args={}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    # Добавление пагинации
    all_options = Options.objects.filter(text_id=Data_id)
    args['options'] = Paginator(all_options, 2).page(page_number)
    args['Data_id']=Data_id
    args['text']=Data.objects.get(id=Data_id)
    return render_to_response('maps.html',args)
def Showmap(request,Opt_id):
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    #html=Options.objects.get(id=Opt_id).html
    script=Options.objects.get(id=Opt_id).script
    div = Options.objects.get(id=Opt_id).div
    args['script'] = script
    args['div'] = div
    return render_to_response("WordMap.html",args)

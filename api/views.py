from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template.context_processors import csrf
import json
from lxml import etree
from time import time
import datetime
import requests
from django.http import JsonResponse
import pandas as pd
from django.http.response import HttpResponse
from infi.clickhouse_orm import models as md
from infi.clickhouse_orm import fields as fd
from infi.clickhouse_orm import engines as en
from infi.clickhouse_orm.database import Database
from django.views.decorators.csrf import csrf_exempt
from api.forms import RequestForm

@csrf_exempt
def CHapi(request):
    def get_clickhouse_data(query,host,connection_timeout=1500):
        r=requests.post(host,params={'query':query},timeout=connection_timeout)
        return r.text
        
    if request.method=='POST':
        order_by=request.POST.get('order_by')
        if order_by=="":
            order_by='city'
        sort_order=request.POST.get('sort_order')
        metrics=request.POST.getlist('metrics[]')
        nb_visits=metrics[0]
        if nb_visits!="":
            nb_visits='LIMIT '+nb_visits
        nb_actions=metrics[1]
        dimensionslist=request.POST.getlist('dimensions[]')
        dimensions=','.join(dimensionslist)
        limit=request.POST.get('limit')
        offset=request.POST.get('offset')
        date1=request.POST.get('date1')
        date2=request.POST.get('date2')
        where=""
        if date1!="" and date2!="":
            where="AND serverDate BETWEEN '%s' AND '%s'"%(date1,date2)
        filt=request.POST.get('filt')
        if filt!="":
            filt='AND '+filt.replace(',',' AND ')
        structure=request.POST.get('structure')
        def SubQuery(d1,i,d2):
            q3='''
            SELECT DISTINCT {dimension2},count(*),sum(actions)
            FROM test.visits
            WHERE {dimension}='{value}' 
            GROUP BY {dimension2}
            '''.format(dimension=dimensionslist[d1],value=str(i),dimension2=dimensionslist[d2])
            l=((get_clickhouse_data(q3,'http://85.143.172.199:8123')).split('\n'))
            l.remove('')
            labels=[]
            visits=[]
            actions=[]
                
            for i in l:
                i=i.split('\t')
                labels.append(i[0])
                visits.append(i[1])
                actions.append(i[2])
            return labels,visits,actions
        
        if structure=="" or structure=="flat":
            q='''SELECT {dimensions},count(*) as nb_visits,sum(actions) as nb_actions FROM test.visits
            WHERE 1 {where}
            {filt}
            GROUP BY {dimensions}
            ORDER BY {order_by} {sort_order}
            {nb_visits}
            FORMAT JSON
            '''.format(dimensions=dimensions,where=where,sort_order=sort_order,order_by=order_by,filt=filt,nb_visits=nb_visits)
            if limit=="" and offset !="":
                resp=json.loads(get_clickhouse_data(q,'http://85.143.172.199:8123'))['data'][int(offset):]
            if limit!="" and offset =="":
                resp=json.loads(get_clickhouse_data(q,'http://85.143.172.199:8123'))['data'][:int(limit)]
            if limit=="" and offset =="":
                resp=json.loads(get_clickhouse_data(q,'http://85.143.172.199:8123'))['data']
            if limit !="" and offset!="":
                resp=json.loads(get_clickhouse_data(q,'http://85.143.172.199:8123'))['data'][int(offset):int(offset)+int(limit)]
            
        else:
            
            #формирование древовидного отчета
            levels=len(dimensionslist)
            sub=[]
            labels=[]
            q2='''
            SELECT DISTINCT {dimension},count(*),sum(actions)
            FROM test.visits
            WHERE 1 {where}
            {filt}
            GROUP BY {dimension}
            {limit}
            '''.format(dimension=dimensionslist[0],limit=nb_visits,where=where,filt=filt)
            tree=[]
            l=((get_clickhouse_data(q2,'http://85.143.172.199:8123')).split('\n'))
            l.remove('')
            labels=[]
            visits=[]
            actions=[]
            for i in l:
                i=i.split('\t')
                labels.append(i[0])
                visits.append(i[1])
                actions.append(i[2])
            for (i,v,a) in zip(labels,visits,actions):
                sub1=[]
                tree.append({'label':i,'segment':dimensionslist[0]+"==",'metrics':{'nb_actions':a,'nb_visits':v},'sub1':sub1})
                if levels>1:
                    labels2,visits2,actions2=SubQuery(0,i,1)
                    for (j,v2,a2) in zip(labels2,visits2,actions2):
                        sub2=[]
                        sub1.append({'label':j,'segment':dimensionslist[0]+"==  "+dimensionslist[1]+"==",'metrics':{'nb_actions':a2,'nb_visits':v2},'sub2':sub2})
                        if levels>2:
                            labels3,visits3,actions3=SubQuery(1,j,2)
                            for (k,v3,a3) in zip(labels3,visits3,actions3):
                                sub3=[]
                                sub2.append({'label':k,'segment':dimensionslist[0]+"==  "+dimensionslist[1]+"== "+dimensionslist[2]+"==",'metrics':{'nb_actions':a3,'nb_visits':v3},'sub3':sub3})   
                                if levels>3:    
                                    labels4,visits4,actions4=SubQuery(2,k,3)
                                    for (m,v4,a4) in zip(labels4,visits4,actions4):
                                        sub4=[]
                                        sub3.append({'label':m,'segment':dimensionslist[0]+"==  "+dimensionslist[1]+"== "+dimensionslist[2]+"== "+dimensionslist[3]+"==",'metrics':{'nb_actions':a4,'nb_visits':v4},'sub4':sub4})
                                        if levels>4:
                                            labels5,visits5,actions5=SubQuery(3,m,4)
                                            for (n,v5,a5) in zip(labels5,visits5,actions5):
                                                sub4.append({'label':n,'segment':dimensionslist[0]+"==  "+dimensionslist[1]+"== "+dimensionslist[2]+"== "+dimensionslist[3]+"== "+dimensionslist[4]+"==",'metrics':{'nb_actions':a5,'nb_visits':v5}})
                                        
                                    
                
            #print(json.dumps(tree))
            resp=tree
        #print(get_clickhouse_data(q,'http://85.143.172.199:8123'))
        
        
        return JsonResponse(json.dumps(resp),safe=False)
    else:
        args={}
        args.update(csrf(request))
        args['form']=RequestForm
        return render_to_response('CHapi.html',args)


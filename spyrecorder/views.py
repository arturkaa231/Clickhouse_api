from django.shortcuts import render,render_to_response
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from time import time
import datetime
from infi.clickhouse_orm import models as md
from infi.clickhouse_orm import fields as fd
from infi.clickhouse_orm import engines as en
from infi.clickhouse_orm.database import Database

from spyrecorder.CHmodels import Actions
# Create your views here.
@csrf_exempt
def AddCH(request):
    def parse_clickhouse_json(jsonBody, db_name, db_host):
        visits_buffer = []
        for i in jsonBody:
            #print(i)
        # inserting data into clickhouse model representation
            insert_visits = Actions(
                user_id=i['user_id'],
                user_name = i['user_name'],
                time = i['time'],
                event_type = i['event_type'],
                screen_name = i['screen_name'],
                app_name = i['app_name'],
                app_productname = i['app_productname'],
                app_version = i['app_version'],
                app_publisher =i['app_publisher'],
                app_file =i['app_file'],
                app_copyright =i['app_copyright'],
                app_language = i['app_language'],
                file_versioninfo =i['file_versioninfo'],
                file_description = i['file_description'],
                file_internalname =i['file_internalname'],
                file_originalname =i['file_originalname'],

            )
            visits_buffer.append(insert_visits)
        db = Database(db_name, db_url=db_host)
            # create table to insert prepared data
        db.create_table(Actions)
            # insert prepared data into database
        db.insert(visits_buffer)
    if request.method == 'POST':
        #print(json.loads(request.body.decode('utf-8')))
        parse_clickhouse_json(json.loads(request.body.decode('utf-8')),'spy_recorder','http://85.143.172.199:8123')
        pass
    else:
        print('')





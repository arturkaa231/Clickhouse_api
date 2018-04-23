import json
import requests
import time
from datetime import datetime, timedelta
from io import BytesIO
import pandas as pd
from infi.clickhouse_orm import models as md
from infi.clickhouse_orm import fields as fd
from infi.clickhouse_orm import engines as en
from infi.clickhouse_orm.database import Database
import pprint
from urllib.parse import urlparse
from urllib.parse import parse_qs
from googleads import oauth2
import xmltodict
import os
from googleads import adwords
from Word2Vec import settings
class Adstat(md.Model):
    idSite=fd.UInt64Field()
    AdCampaignId=fd.StringField()
    AdBannerId=fd.StringField()
    AdDeviceType=fd.StringField()
    AdGroupId=fd.StringField()
    AdKeywordId=fd.StringField()
    AdPosition=fd.StringField()
    AdPositionType=fd.StringField()
    AdRegionId=fd.StringField()
    AdRetargetindId=fd.StringField()
    AdPlacement=fd.StringField()
    AdTargetId=fd.StringField()
    AdvertisingSystem=fd.StringField()
    DRF=fd.StringField()
    campaignContent=fd.StringField()
    campaignKeyword=fd.StringField()
    campaignMedium=fd.StringField()
    campaignName=fd.StringField()
    campaignSource=fd.StringField()
    StatDate=fd.DateField()
    StatDateTime = fd.DateTimeField()
    Impressions=fd.UInt64Field()
    Clicks=fd.UInt64Field()
    Cost=fd.Float64Field()
    IntegrationId=fd.StringField()
    Sign = fd.Int8Field()
    engine = en.CollapsingMergeTree(('StatDate','IntegrationId'),('StatDate','IntegrationId','idSite','AdCampaignId','AdBannerId','AdDeviceType','AdGroupId','AdKeywordId','AdPosition'
                                                                  ,'AdPositionType','AdRegionId','AdRetargetindId','AdPlacement','AdTargetId','AdvertisingSystem','DRF',
                                                                  'campaignContent','campaignKeyword','campaignMedium','campaignName','campaignSource','StatDateTime'),'Sign')
def get_clickhouse_data(query, host, connection_timeout=1000050):
    """Метод для обращения к базе данных CH"""
    r = requests.post(host, params={'query': query}, timeout=connection_timeout)

    return r.text
def chunks(l,n):
    for i in range(0,len(l),n):
        yield l[i:i+n]

def ga_stat_daily(integration, period1, period2):
    '''
    integration={
            "id": 1,
            "credential": {
                "expires_in": 31536000,
                "token_type": "bearer",
                "access_token": "AQAAAAALL2cIAAGQs2VDPflIVkTSsKxS-uLw9Rk",
                "refresh_token": "1:jogkSFI-GF5Xwd2X:_bgdvu3yWWEnMfZPJoZbkZodqpnFszGMQ3fetlSbJn-fd9w7SJH6:NSLR-Jf7eYA1LzRvs9t32w"
            },
            "active": true,
            "settings": {
                "ad_client_id": 18
            },
            "type": 3,
            "site": 35
        }

    period1=date('2018-01-01')
    period2=date('2018-02-01')

    '''
    past_hour = "'" + (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:00:00') + "'"
    StatDate = "'" + str(datetime.now().strftime('%Y-%m-%d')) + "'"
    if int(datetime.now().strftime('%H')) == 1:
        past_hour = "'" + (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 23:00:00') + "'"
        StatDate = "'" + str((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')) + "'"
    client = json.loads(requests.get('https://s.analitika.online/api/ad/ad_clients?id={id}'.format(id=integration['settings']['ad_client_id']),headers=headers).content.decode('utf-8'))['results'][0]
    print(client)
    # Проверка. Берем из таблицы данные за прошлый час и сравниваем с текущими данными, если показатели изменились, то записываем в таблицу эту разницу
    query = """SELECT toString(idSite),AdCampaignId,AdBannerId,AdDeviceType,AdGroupId,AdKeywordId,AdPosition,AdPositionType,AdRegionId,AdRetargetindId,AdPlacement,AdTargetId,AdvertisingSystem,DRF,StatDate,toString(IntegrationId),Impressions,Clicks,Cost FROM CHdatabase.adstat WHERE StatDate={StatDate}  FORMAT JSON""".format(
        StatDate=StatDate,
        hour=past_hour)
    last_day = json.loads(get_clickhouse_data(query, 'http://46.4.81.36:8123'))['data']
    stat_days = []
    delta = int((period2 - period1).days)
    total_sum = 0
    total_clicks = 0
    ad_units = json.loads(requests.get( 'https://s.analitika.online/api/ad/ad_units?adclient__id={id}'.format(id=integration['settings']['ad_client_id']),headers=headers).content.decode('utf-8'))
    banners = ad_units['results'][0]['banners']
    keywords = ad_units['results'][0]['keywords']
    campaigns = ad_units['results'][0]['campaigns']
    adgroups = ad_units['results'][0]['ad_groups']
    d_t = datetime.now()
    REFRESH_TOKEN = integration['credential']['refresh_token']
    oauth2_client = oauth2.GoogleRefreshTokenClient(settings.ADWORDS_CLIENT_ID, settings.ADWORDS_CLIENT_SECRET,
                                                    REFRESH_TOKEN)

    adwords_client = adwords.AdWordsClient(settings.ADWORDS_DEVELOPER_TOKEN, oauth2_client, settings.ADWORDS_USER_AGENT,
                                           client_customer_id=client['client_id'])
    report_downloader = adwords_client.GetReportDownloader(version='v201705')
    report = {
        'reportName': 'Last 7 days AD_PERFORMANCE_REPORT',
        'dateRangeType': 'CUSTOM_DATE',
        'reportType': 'AD_PERFORMANCE_REPORT',
        'downloadFormat': 'XML',
        'selector': {
            'dateRange': {'min': period1.strftime("%Y%m%d"), 'max': period2.strftime("%Y%m%d")},
            'fields': ['CampaignId', 'AdGroupId', 'Device', 'Slot', 'AdNetworkType2', 'AveragePosition',
                       'CreativeFinalUrls', 'CreativeTrackingUrlTemplate', 'Id', 'CriterionId', 'Date',
                       'Cost', 'Clicks', 'Impressions'],
        }
    }

    raw_data = report_downloader.DownloadReportAsString(report, skip_report_header=True, skip_column_header=True,
                                                        skip_report_summary=True)

    if len(raw_data) > 0:
        v = json.dumps(xmltodict.parse(raw_data))
        ad_stat = json.loads(v.replace('@', ''))['report']['table']['row']
    else:
        ad_stat = []

    temp = []
    kws_stat = {}
    device_map = {
        'Mobile devices with full browsers': 'mobile',
        'Tablets with full browsers': 'tablet',
        'Computers': 'desktop'
    }
    total_sum = 0
    total_clicks = 0

    if type(ad_stat) is not list:
        ad_stat = [ad_stat]
    for stat in chunks(ad_stat, 10000):
        temp = []
        ad_buffer = []
        for s in stat:
            if str(s['keywordID']) in keywords:
                s['keyword'] = keywords[s['keywordID']]['keyword']
            else:
                s['keyword'] = 'Не определено'

            account = client['tracking_template']

            if str(s['campaignID']) in campaigns:
                campaign = campaigns[str(s['campaignID'])]
            else:
                tracking_template = {}
                url = parse_qs(
                    urlparse(s['trackingTemplate'].replace('#', '').replace('{lpurl}', 'http://test.ru/?')).query)
                if 'utm_source' in url:
                    tracking_template['utm_source'] = url['utm_source'][0]
                if 'utm_medium' in url:
                    tracking_template['utm_medium'] = url['utm_medium'][0]
                if 'utm_campaign' in url:
                    tracking_template['utm_campaign'] = url['utm_campaign'][0]
                if 'utm_term' in url:
                    tracking_template['utm_term'] = url['utm_term'][0]
                if 'utm_content' in url:
                    tracking_template['utm_content'] = url['utm_content'][0]

                campaign = {
                    'name': s['campaign'],
                    'tracking_template': tracking_template
                }
                if not s['adID'] in banners:

                    tracking_template = {'adGroupId': s['adGroupID'], 'tracking_template': {}}
                    url = parse_qs(urlparse(
                        json.loads(s['finalURL'])[0].replace('#', '').replace('{lpurl}', 'http://test.ru/?')).query)
                    if 'utm_source' in url:
                        tracking_template['tracking_template']['utm_source'] = url['utm_source'][0]
                    if 'utm_medium' in url:
                        tracking_template['tracking_template']['utm_medium'] = url['utm_medium'][0]
                    if 'utm_campaign' in url:
                        tracking_template['tracking_template']['utm_campaign'] = url['utm_campaign'][0]
                    if 'utm_term' in url:
                        tracking_template['tracking_template']['utm_term'] = url['utm_term'][0]
                    if 'utm_content' in url:
                        tracking_template['tracking_template']['utm_content'] = url['utm_content'][0]

                    banners[s['adID']] = tracking_template
                if not s['adGroupID'] in adgroups:
                    adgroups[s['adGroupID']] = {'tracking_template': {}}

            if s['adID'] in banners:
                utms = banners[str(s['adID'])]
                adgroup = adgroups[utms['adGroupId']]
                ##добавляем шаблон отслеживания из ключа
                if str(s['keywordID']) in keywords:
                    utms = {**utms, **keywords[s['keywordID']]}

                if not 'utm_source' in utms:
                    utms['utm_source'] = \
                    google_check_tracking_templates('utm_source', account, campaign['tracking_template'],
                                                    adgroup['tracking_template'],
                                                    banners[str(s['adID'])]['tracking_template'])['utm_source']
                if not 'utm_medium' in utms:
                    utms['utm_medium'] = \
                    google_check_tracking_templates('utm_medium', account, campaign['tracking_template'],
                                                    adgroup['tracking_template'],
                                                    banners[str(s['adID'])]['tracking_template'])['utm_medium']
                if not 'utm_campaign' in utms:
                    utms['utm_campaign'] = \
                    google_check_tracking_templates('utm_campaign', account, campaign['tracking_template'],
                                                    adgroup['tracking_template'],
                                                    banners[str(s['adID'])]['tracking_template'])['utm_campaign']
                if not 'utm_term' in utms:
                    utms['utm_term'] = \
                    google_check_tracking_templates('utm_term', account, campaign['tracking_template'],
                                                    adgroup['tracking_template'],
                                                    banners[str(s['adID'])]['tracking_template'])['utm_term']
                if not 'utm_content' in utms:
                    utms['utm_content'] = \
                    google_check_tracking_templates('utm_content', account, campaign['tracking_template'],
                                                    adgroup['tracking_template'],
                                                    banners[str(s['adID'])]['tracking_template'])['utm_content']

                new_utm = match_google_utm_experiment(utms, s)
                if len(new_utm) == 0:
                    new_utm = {'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': 'не определено',
                               'utm_term': 'не определено', 'utm_content': 'не определено'}

            else:

                new_utm = {'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': 'не определено',
                           'utm_term': 'не определено', 'utm_content': 'не определено'}

            s['Cost'] = (int(s['cost']) / 1000000)
            s['Clicks'] = int(s['clicks'])
            s['Impressions'] = int(s['impressions'])
            if s['topVsOther'] == 'Google Display Network':
                s['position_type'] = 'none'
            elif s['topVsOther'] == 'Google search: Top':
                s['position_type'] = 'premium'
            elif s['topVsOther'] == 'Google search: Other':
                s['position_type'] = 'other'
            total_sum += s['Cost']
            total_clicks += s['Clicks']
            print(s)
            try:
                position_type=str(s['position_type'])
            except:
                position_type=''

            values = [str(integration['site_db_id']), str(s['campaignID']), str(s['adID']), str(s['device']),
                      str(s['adGroupID']), str(s['keywordID']),
                      str(s['avgPosition']),position_type, '', '',
                      str(s['networkWithSearchPartners']), '', "google adwords", "", str(new_utm['utm_content']),
                      str(new_utm['utm_term']), str(new_utm['utm_medium']), str(new_utm['utm_campaign']), str(new_utm['utm_source']), str(s['day']),
                      str(hour), str(s['Impressions']), str(s['Clicks']), str(s['Cost']), str(integration['id']),
                      str(1)]
            compare_values = values[:14]
            compare_values.append(values[19])
            compare_values.append(values[24])
            new_values = values

            for string in last_day:
                if list(string.values())[:-3] == compare_values:
                    NewImpressions = int(values[21]) - string['Impressions']
                    NewClicks = int(values[22]) - string['Clicks']
                    NewCost = float(values[23]) - string['Cost']
                    if NewImpressions != 0 and NewClicks != 0 and NewCost != 0:
                        new_values[21] = str(NewImpressions)
                        new_values[22] = str(NewClicks)
                        new_values[23] = str(NewCost)
                        break
                    else:
                        new_values = 0
                        break
            if new_values != 0:
                pass
            else:
                continue
            print(new_values)
            insert = Adstat(
                idSite=int(new_values[0]),
                AdCampaignId=new_values[1],
                AdBannerId=new_values[2],
                AdDeviceType=new_values[3],
                AdGroupId=new_values[4],
                AdKeywordId=new_values[5],
                AdPosition=new_values[6],
                AdPositionType=new_values[7],
                AdRegionId=new_values[8],
                AdRetargetindId=new_values[9],
                AdPlacement=new_values[10],
                AdTargetId=new_values[11],
                AdvertisingSystem=new_values[12],
                DRF=new_values[13],
                campaignContent=new_values[14],
                campaignKeyword=new_values[15],
                campaignMedium=new_values[16],
                campaignName=new_values[17],
                campaignSource=new_values[18],
                StatDate=new_values[19],
                StatDateTime=new_values[20],
                Impressions=int(new_values[21]),
                Clicks=int(new_values[22]),
                Cost=float(new_values[23]),
                IntegrationId=new_values[24],
                Sign=int(new_values[25]),
            )
            ad_buffer.append(insert)

        db = Database('CHdatabase', db_url='http://46.4.81.36:8123')
        db.insert(ad_buffer)
    print('total sum' + str(total_sum))
    print('total clicks' + str(total_clicks))


def google_check_tracking_templates(utm, account, campaign, adgroup, banner):
    if utm == 'utm_source':
        new_utm = {'utm_source': 'google'}
    elif utm == 'utm_medium':
        new_utm = {'utm_medium': 'cpc'}
    else:
        new_utm = {utm: 'не определено'}
    if utm in account:
        new_utm[utm] = account[utm]
    if utm in campaign:
        new_utm[utm] = campaign[utm]
    if utm in adgroup:
        new_utm[utm] = adgroup[utm]
    if utm in banner:
        new_utm[utm] = banner[utm]
    return new_utm


def match_google_utm_experiment(utms, s):
    new_utm = {}
    for k, v in utms.items():
        # print (utms)
        if 'utm' in k:
            new_utm[k] = str(utms[k]).replace('{creative}', s['adID']).replace('{campaignid}', s['campaignID']) \
                .replace('{keyword}', s['keyword']).replace('{phrase_id}', s['keywordID'])
    return new_utm
headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxOSwiZW1haWwiOiIiLCJ1c2VybmFtZSI6ImFydHVyIiwiZXhwIjoxNTE4MTIxNDIyfQ._V0PYXMrE2pJlHlkMtZ_c-_p0y0MIKsv8o5jzR5llpY',
            'Content-Type': 'application/json'}
if int(datetime.now().strftime('%H')) == 0:
    hour =(datetime.now()- timedelta(days=1)).strftime('%Y-%m-%d 23:00:00')
    DateFrom = datetime.now() - timedelta(days=1)
else:
    DateFrom = datetime.now()
    hour = (datetime.now()- timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
for res in json.loads(requests.get('https://s.analitika.online/api/integrations?all=1',headers=headers).content.decode('utf-8'))['results']:
    if res['type']==4:
        ga_stat_daily(res,DateFrom,DateFrom)

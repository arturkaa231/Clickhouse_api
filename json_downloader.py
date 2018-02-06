import requests
import json
def get_clickhouse_data(query,host,connection_timeout=1500):
    r=requests.post(host,params={'query':query},timeout=connection_timeout)
    return r.text
#Метод для получения json-а из апи
def get_json(source):

    try:
        response = requests.get(source)

    except (requests.exceptions.ChunkedEncodingError) as e:
        response = requests.get(source)

    return response.content.decode('utf-8')
query="INSERT INTO CHdatabase.adstat VALUES "

JSON=get_json('https://bi.analitika.online/get_stat_next/?smart=1')
'''JSON=[{'keyword': 'евроремонт квартир', 'spend': 10.0, 'shows': 5, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_kvartir_poisk', 'utm_term': 'евроремонт квартир', 'clicks': 0, 'campaign': 26701970, 'utm_medium': 'cpc', 'banner': '4093378306', 'utm_content': 'luboi_slozhnosti', 'adclient': 468}, {'keyword': 'ремонт в новостройке', 'spend': 0.0, 'shows': 9, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_novostroiki_poisk', 'utm_term': 'ремонт в новостройке', 'clicks': 0, 'campaign': 26701747, 'utm_medium': 'cpc', 'banner': '4084722422', 'utm_content': 'luboi_slozhnosti', 'adclient': 468}, {'keyword': 'ремонт в новостройке', 'spend': 0.0, 'shows': 2, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_novostroiki_poisk', 'utm_term': 'ремонт в новостройке', 'clicks': 0, 'campaign': 26701747, 'utm_medium': 'cpc', 'banner': '4084722441', 'utm_content': 'fiksirovannaya_stoimost', 'adclient': 468}, {'keyword': 'ремонт и отделка помещений', 'spend': 0.0, 'shows': 2, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_pomescheniya_poisk', 'utm_term': 'ремонт и отделка помещений', 'clicks': 0, 'campaign': 26703227, 'utm_medium': 'cpc', 'banner': '4093358182', 'utm_content': 'luboi_slozhnosti', 'adclient': 468}, {'keyword': 'ремонт гостиниц', 'spend': 40.0, 'shows': 1, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_pomescheniya_poisk', 'utm_term': 'ремонт гостиниц', 'clicks': 1, 'campaign': 26703227, 'utm_medium': 'cpc', 'banner': '4093358175', 'utm_content': 'fiksirovannaya_stoimost', 'adclient': 468}, {'keyword': 'ремонт загородного дома', 'spend': 0.0, 'shows': 1, 'stat_date': '2017-11-01', 'utm_source': 'yandex', 'utm_campaign': 'biznes_remont_doma_poisk', 'utm_term': 'ремонт загородного дома', 'clicks': 0, 'campaign': 26701463, 'utm_medium': 'cpc', 'banner': '4085042722', 'utm_content': 'luboi_slozhnosti', 'adclient': 468}]'''

#print(JSON)
JSON=json.loads(JSON)

list_of_keys=['adclient','campaign','stat_date','banner','keyword','shows','clicks','spend','utm_source','utm_medium','utm_campaign','utm_term','utm_content'] #список полей базы

#кладем объекты из json-а в бд по 20 записей за раз
for obj in JSON:
    data=[]
    for i in list_of_keys:
        if i in ['adclient','campaign','shows','clicks','spend']:
            data.append(str(obj[i]))
        else:
            data.append("'"+str(obj[i])+"'")
#print('данные до:')
#print(data)


#делаем запрос в базу для получения текущих значений сумм по кликам, показам и тратам
    compare_query='''SELECT sum(shows) as shows,sum(clicks) as clicks,sum(spend) as spend
FROM CHdatabase.adstat
WHERE adclient={adcl} AND banner={ban} AND stat_date={st} AND keyword={kw} FORMAT JSON'''.format(adcl=data[0],ban=data[3],st=data[2],kw=data[4])
    compare_response=json.loads(get_clickhouse_data(compare_query,'http://85.143.172.199:8123'))['data']
#если такие имеются, сравниваем их с теми, что необходимо занести в базу, если нет-переходим к следующему картежу
    if compare_response!=[]:
        new_sum=[data[5],data[6],data[7]]
#print(new_sum)

        old_sum=[compare_response[0]['shows'],compare_response[0]['clicks'],str(round(float(compare_response[0]['spend']),2))]
#print(old_sum)
        if new_sum==old_sum:
#print('данные свежи')
            continue
        else:
            data[5]=str(int(new_sum[0])-int(old_sum[0]))
            data[6]=str(int(new_sum[1])-int(old_sum[1]))
            data[7]=str(round(float(new_sum[2])-float(old_sum[2]),2))
#print('данныепосле:')
#print(data)

    get_clickhouse_data(query+"("+','.join(data)+")",'http://85.143.172.199:8123')

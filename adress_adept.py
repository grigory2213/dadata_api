import pandas as pd
import requests
import json
import datetime


now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y")
print(now)

df_adress = pd.read_excel('dadata/XLSX Worksheet.xlsx')
df_adress['adress'] = df_adress['adress'].str.lower()
df_adress['adress'] = df_adress['adress'].str.replace("№","")
print(df_adress)

def get_full_adress(adress):
    
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Token 8f87c1c11a0ab5134fe621044cfa89b35d082563',
    }

    json_data = {
        'query': f'{adress}',
        'count': 1,
    }   

    response = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address', headers=headers, json=json_data).json()
    return response



def getting_adress():
    new_adress_data = pd.DataFrame()
    cannnot_find = []
    for i in range(len(df_adress)):
        adress = df_adress["adress"][i]
        try:
            result = get_full_adress(adress)
            with open(f'dadata/{i}.json', 'w') as json_file:
                json.dump(result, json_file)
            
            with open(f'dadata/{i}.json', 'r') as f:
                json_data = json.loads(f.read())
            df = pd.json_normalize(json_data['suggestions'])
            df = df[['unrestricted_value', 'data.region_with_type', 'data.postal_code', 'data.country_iso_code', 'data.city','data.settlement', 'data.street', 'data.street_type', 'data.house', 'data.house_type', 'data.settlement', 'data.geo_lat', 'data.geo_lon']]
            new_adress_data = new_adress_data.append(df)
        except:
            print('скип')
            cannnot_find.append(str(adress))
            
            
    
    new_adress_data.to_excel('dadata/new_adress.xlsx')
    print("Не смог найти: ", len(cannnot_find))
    print(cannnot_find)
    
    
    df = pd.DataFrame(cannnot_find)
    df.to_excel('Не_нашлись.xlsx')
    print(df.info())
    return result

getting_adress()

new = pd.read_excel('dadata/new_adress.xlsx')

sm = pd.read_excel('dadata/Shopmetrics.xlsx')

print(new['data.city'])
print(new['data.settlement'])

sm['Location Name'] = new['data.region_with_type']
sm['Address'] = new['data.street_type'] + '.' + ' ' + new['data.street'] + ',' + ' ' + new['data.house_type'] + '.' + ' ' + new['data.house']
sm['City'] = new['data.city']
sm['Country'] = new['data.country_iso_code']
sm['Postal Code'] = new['data.postal_code']
sm['Latitude'] = new['data.geo_lat']
sm['Longitude'] = new['data.geo_lon']
for i in range(len(new)):
    sm['Store ID'][i] = '101'+ str(now) + str(i)


print(sm)
sm.to_excel('new_adress1.xlsx')

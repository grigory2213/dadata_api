import pandas as pd
import requests
import json
from dadata import Dadata


df_gerioni = pd.read_excel('/home/grigory/Local/Work/dadata_api/Обозначения Регионы.xlsx')
df_adress = pd.read_excel('dadata_api/XLSX Worksheet.xlsx')
df_adress['adress'] = df_adress['adress'].str.lower()
df_adress['adress'] = df_adress['adress'].str.replace("№","")
print(df_adress)

def get_full_adress(adress):
    
    token = "8f87c1c11a0ab5134fe621044cfa89b35d082563"
    secret = "dd0dc733834a73c3e13006ff12f792737c9954a4"
    dadata = Dadata(token, secret)
    result = dadata.clean("address", f'{adress}')
    print(result)

    return result



def getting_adress():
    new_adress_data = pd.DataFrame()
    cannnot_find = []
    for i in range(len(df_adress)):
        adress = df_adress["adress"][i]
        print(adress)
        try:
            result = get_full_adress(adress)
            print(result)
            with open(f'dadata_api/{i}.json', 'w') as json_file:
                json.dump(result, json_file)
            
            with open(f'dadata_api/{i}.json', 'r') as f:
                json_data = json.loads(f.read())
            df = pd.json_normalize(json_data)
            df = df[['region_with_type', 'postal_code', 'country_iso_code', 'city','settlement', 'street', 'street_type', 'house', 'house_type', 'settlement', 'geo_lat', 'geo_lon']]
            df['Store ID'] = ''
            df['Store ID']= df_adress['Store ID'][i]
            df['Name'] = ''
            df['Name'] = df_adress['Name'][i]
            #df['Phone'][i] = df_adress['Phone'][i]
            
            #df['Location Hours'][i] = df_adress['Location Hours'][i]
            
            new_adress_data = new_adress_data.append(df)
            
        except:
            print('скип')
            cannnot_find.append(str(adress))
            
            
    
    new_adress_data.to_excel('dadata_api/new_adress.xlsx')
    print("Не смог найти: ", len(cannnot_find))
    print(cannnot_find)
    
    
    df = pd.DataFrame(cannnot_find)
    df.to_excel('Не_нашлись.xlsx')
    print(df.info())
    return result

#getting_adress()

new = pd.read_excel('dadata_api/new_adress.xlsx')

sm = pd.read_excel('dadata_api/Shopmetrics.xlsx')

sm['Store ID'] = new['Store ID']
sm['Location Name'] = new['Name']
sm['Address'] = new['street_type'] + '.' + ' ' + new['street'] + ',' + ' '  + new['house']
sm['City'] = new['city']
sm['Country'] = new['country_iso_code']
sm['Postal Code'] = new['postal_code']
sm['Latitude'] = new['geo_lat']
sm['Longitude'] = new['geo_lon']
#sm['Phone'] = new['Phone']
#sm['Location Hours'] = new['Location Hours']

sm['Address']  = sm['Address'].str.replace('ш. ', 'шоссе ')

sm = pd.merge(sm, df_gerioni, how = 'left', left_on = 'City', right_on = 'город')
sm = sm.drop(['город'], axis = 1)

print(sm)
sm.to_excel('new_adress1.xlsx')

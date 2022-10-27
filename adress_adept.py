from dadata import Dadata
import pandas as pd
import requests
import json

# token = "8f87c1c11a0ab5134fe621044cfa89b35d082563"
# dadata = Dadata(token)

df_adress = pd.read_excel('dadata/XLSX Worksheet.xlsx')


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
    nothing_str = pd.DataFrame()
    for i in range(len(df_adress)):
        adress = df_adress["adress"][i]
        try:
            result = get_full_adress(adress)
            
            #print(result)
            with open(f'dadata/{i}.json', 'w') as json_file:
                json.dump(result, json_file)
            
            with open(f'dadata/{i}.json', 'r') as f:
                json_data = json.loads(f.read())
            df = pd.json_normalize(json_data['suggestions'])
            #print(df.info())
            df = df[['unrestricted_value', 'data.postal_code', 'data.country', 'data.city','data.settlement', 'data.street', 'data.house', 'data.geo_lat', 'data.geo_lon']]
            #print(df.info())
            new_adress_data = new_adress_data.append(df)
        except:
            print('скип')
    
    new_adress_data.to_excel('dadata/new_adress.xlsx')
    return result

getting_adress()
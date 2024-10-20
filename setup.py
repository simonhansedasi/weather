import tarfile
import os
import json
import pandas as pd

if not os.path.exists('data/Seattle_47_606139_-122_332848_6706e314ebe2e0000809c1af.csv'):
    tarball_path = 'data/Seattle.tar.gz'
    extract_path = 'data/'

    with tarfile.open(tarball_path, 'r:gz') as tar:
        tar.extractall(path=extract_path) 
        
    print('Extracted tarball')
    
    
if os.path.exists('data/Seattle_47_606139_-122_332848_6706e314ebe2e0000809c1af.csv') and not os.path.exists('data/data.json'):

    pth = 'data/'

    df = pd.read_csv(os.path.join(pth,'Seattle_47_606139_-122_332848_6706e314ebe2e0000809c1af.csv'))

    feats = [
        'dt','temp_min','temp','temp_max','dew_point','pressure',
        'humidity','wind_speed','wind_deg','wind_gust','clouds_all',
        'rain_1h','rain_3h','snow_1h','snow_3h'
    ]
    df[['temp_min','temp','temp_max','dew_point']] = df[['temp_min','temp','temp_max','dew_point']] - 273.15 ## convert kelvin to C
    def listify(data):
        return data.tolist()  


    data = {}

    for feat in feats:
        data[feat] = listify(df[feat])


    # print(data.keys())
    
    # data_serializable = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in data.items()}

    
    
    

    with open('data/data.json', 'w') as json_file:
        json.dump(data, json_file)
    print('data saved as .json file')
    
elif os.path.exists('data/Seattle_47_606139_-122_332848_6706e314ebe2e0000809c1af.csv') and os.path.exists('data/data.json'):
    print('data already extracted successfully')

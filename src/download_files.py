import requests
import pandas as pd
import os
from datetime import datetime
from datetime import date
import calendar 
from unidecode import unidecode
from src.logger import log
from src.preprocessing_data import process_data, fix_data, province_file, cinema_file, category_file, build_main_dataSet

now = datetime.now()
today=date.today()
monthName = calendar.month_name[today.month]


URL = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/'
MAIN_PATH = 'files/mains_csv'

def get_mainDataSet():
    museos = download_file('museos', '4207def0-2ff7-41d5-9095-d42ae8207a5d')
    bibliotecas = download_file('bibliotecas', '01c6c048-dbeb-44e0-8efa-6944f73715d7')
    cines = download_file('cines', 'f7a8edb8-9208-41b0-8f19-d72811dcea97')
    pd_data = build_main_dataSet([museos,bibliotecas,cines])
    return pd_data

def download_file(data, idDataset):
    path = f'files/{data}/{today.year}-{monthName}'
    file_path = f"{path}/{data}-{today}.csv"

    if not os.path.exists(path):
        os.makedirs(path)

    url = URL + idDataset + '/download/.csv'
    try:
        response = requests.get(url)
    except:
        log(f'Error on download {data} file', 'error')
    if response.ok:
        open(file_path, "wb").write(response.content)
    
    df = process_data(file_path) 
    return df

def get_files():
    if not os.path.exists(MAIN_PATH):
            os.makedirs(MAIN_PATH)

    mainDataSet = get_mainDataSet()
    try:
        mainDataSet.to_csv(f'{MAIN_PATH}/main.csv', index=False)
        log('Main Data Set Download', 'info')
    except:
        print('Error on get Main Data Set')
        log('Error on get Main data set', 'error')
    
    province_file(mainDataSet).to_csv(f'{MAIN_PATH}/province.csv', index=False)    
    category_file(mainDataSet).to_csv(f'{MAIN_PATH}/category.csv', index=False)  

    cinema_file().to_csv(f'{MAIN_PATH}/cinema.csv', index=False)

# get_files()
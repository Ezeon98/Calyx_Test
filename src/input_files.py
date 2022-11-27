import requests
import pandas as pd
import os
from datetime import datetime
import calendar 
from unidecode import unidecode
from src.logger import log

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
currentDate = f'{currentDay}-{currentMonth}-{currentYear}'
monthName = calendar.month_name[currentMonth]

COLUMNS = ['cod_loc', 'idprovincia','iddepartamento', 'categoria', 
           'provincia','localidad', 'nombre',
           'direccion','cp','telefono','mail','web']

URL = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/'
MAIN_PATH = 'mains_csv'

def get_mainDataSet():
    museos = download_file('museos', '4207def0-2ff7-41d5-9095-d42ae8207a5d')
    bibliotecas = download_file('bibliotecas', '01c6c048-dbeb-44e0-8efa-6944f73715d7')
    cines = download_file('cines', 'f7a8edb8-9208-41b0-8f19-d72811dcea97')
    pd_data = pd.concat([museos,bibliotecas,cines])
    pd_data['provincia'] = pd_data['provincia'].apply(unidecode)
    return pd_data

def download_file(data, idDataset):
    path = f'{data}/{currentYear}-{monthName}'
    file_path = f"{path}/{data}-{currentDate}.csv"

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

def process_data(path):
    df2 = pd.read_csv(path)
    fix_data(df2)
    df2 = df2.filter(items=COLUMNS)  
    return df2

def fix_data(df2):
    df2.columns = df2.columns.str.lower()
    df2.columns = [unidecode(col) for col in df2.columns]
    if 'domicilio' in df2.columns:
        df2.rename(columns = {'domicilio':'direccion'}, inplace = True)
    if 'cod_localidad' in df2.columns:
        df2.rename(columns = {'cod_localidad':'cod_loc'}, inplace = True)
    if 'id_provincia' in df2.columns:
        df2.rename(columns = {'id_provincia':'idprovincia'}, inplace = True)
    if 'id_departamento' in df2.columns:
        df2.rename(columns = {'id_departamento':'iddepartamento'}, inplace = True)
    for c in COLUMNS:
        if c not in df2.columns:
            df2[c] = None
    return df2

def category_file(pd_data):

    category_df = pd.DataFrame({"Categoria":['Salas de cine',
                                     'Bibliotecas Populares',
                                     'Espacios de Exhibición Patrimonial'],
                        "Cantidad":[len(pd_data[pd_data['categoria']=='Salas de cine']),
                                    len(pd_data[pd_data['categoria']=='Bibliotecas Populares']),
                                    len(pd_data[pd_data['categoria']=='Espacios de Exhibición Patrimonial'])]})
    
    return category_df

def province_file(pd_data):
    
    province_df = pd_data[['provincia']]
    province_df = province_df.groupby(["provincia"])["provincia"].count()
    province_df = province_df.reset_index(name='cantidad')
    
    return province_df

def cinema_file():
    file_path = f"cines/{currentYear}-{monthName}/cines-{currentDate}.csv"
    df2 = pd.read_csv(file_path)
    df2 = df2.filter(items=['provincia','pantallas', 'butacas','espacio_incaa'])
    df2['espacio_incaa'] = df2['espacio_incaa'].replace(['Si','No'], [1,0])
    df2 = df2.groupby(["provincia"]).sum()
    df2=df2.reset_index()
    return df2

def get_files():
    if not os.path.exists(MAIN_PATH):
            os.makedirs(MAIN_PATH)
    try:
        get_mainDataSet().to_csv(f'{MAIN_PATH}/main.csv', index=False)
        log('Main Data Set Download', 'info')
    except:
        print('Error on get Main Data Set')
        log('Error on get Main data set', 'error')
    
    province_file(get_mainDataSet()).to_csv(f'{MAIN_PATH}/province.csv', index=False)    
    category_file(get_mainDataSet()).to_csv(f'{MAIN_PATH}/category.csv', index=False)  

    cinema_file().to_csv(f'{MAIN_PATH}/cinema.csv', index=False)

# get_files()
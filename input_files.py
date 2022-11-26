import requests
import pandas as pd
import os
from datetime import datetime
import calendar 
from unidecode import unidecode

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
currentDate = f'{currentDay}-{currentMonth}-{currentYear}'
monthName = calendar.month_name[currentMonth]

columns = ['cod_loc', 'idprovincia','iddepartamento', 'categoria', 
           'provincia','localidad', 'nombre',
           'direccion','cp','telefono','mail','web']

main_url = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/'

def get_dataSet():
    museos = download_file('museos', '4207def0-2ff7-41d5-9095-d42ae8207a5d')
    bibliotecas = download_file('bibliotecas', '01c6c048-dbeb-44e0-8efa-6944f73715d7')
    cines = download_file('cines', 'f7a8edb8-9208-41b0-8f19-d72811dcea97')
    pd_data = pd.concat([museos,bibliotecas,cines])
    return pd_data

def download_file(data, idDataset):
    
    url = main_url + idDataset + '/download/.csv'
    response = requests.get(url)
    
    path = f'{data}/{currentYear}-{monthName}'
    file_path = f"{path}/{data}-{currentDate}.csv"
    if not os.path.exists(path):
        os.makedirs(path)
    open(file_path, "wb").write(response.content)
    
    df = process_data(file_path) 
    return df

def process_data(path):
    df2 = pd.read_csv(path)
    fix_data(df2)
    df2 = df2.filter(items=columns)  
    return df2

def fix_data(df2):
    df2.columns = df2.columns.str.lower()
    df2.columns = [unidecode(col) for col in df2.columns]
    # if 'telefono' not in df2.columns:
    #     df2['telefono'] = None
    # if 'mail' not in df2.columns:
    #     df2['mail'] = None
    if 'domicilio' in df2.columns:
        df2.rename(columns = {'domicilio':'direccion'}, inplace = True)
    if 'cod_localidad' in df2.columns:
        df2.rename(columns = {'cod_localidad':'cod_loc'}, inplace = True)
    if 'id_provincia' in df2.columns:
        df2.rename(columns = {'id_provincia':'idprovincia'}, inplace = True)
    if 'id_departamento' in df2.columns:
        df2.rename(columns = {'id_departamento':'iddepartamento'}, inplace = True)
    for c in columns:
        if c not in df2.columns:
            df2[c] = None
    return df2

def other_tables(pd_data):
    pd_data['provincia'] = pd_data['provincia'].apply(unidecode)
    category_df = pd.DataFrame({"Categoria":['Salas de cine',
                                     'Bibliotecas Populares',
                                     'Espacios de Exhibición Patrimonial'],
                        "Cantidad":[len(pd_data[pd_data['categoria']=='Salas de cine']),
                                    len(pd_data[pd_data['categoria']=='Bibliotecas Populares']),
                                    len(pd_data[pd_data['categoria']=='Espacios de Exhibición Patrimonial'])]})
    
    province_df = pd_data[['provincia']]
    province_df = province_df.groupby(["provincia"])["provincia"].count()
    province_df = province_df.reset_index(name='cantidad')
    
    return category_df,province_df

def cinema_table():
    file_path = f"cines/{currentYear}-{monthName}/cines-{currentDate}.csv"
    df2 = pd.read_csv(file_path)
    df2 = df2.filter(items=['provincia','pantallas', 'butacas','espacio_incaa'])
    df2['espacio_incaa'] = df2['espacio_incaa'].replace(['Si','No'], [1,0])
    df2 = df2.groupby(["provincia"]).sum()
    df2=df2.reset_index()
    return df2


if not os.path.exists('Mains CSVs'):
        os.makedirs('Mains CSVs')

pd_data = get_dataSet()
pd_data.to_csv('Mains CSVs/main.csv', index=False)

cinema_df = cinema_table()
cinema_df.to_csv('Mains CSVs/cinema.csv', index=False)

category_df,province_df = other_tables(pd_data)

category_df.to_csv('Mains CSVs/category.csv', index=False)
province_df.to_csv('Mains CSVs/province.csv', index=False)

# print(cinema_df)

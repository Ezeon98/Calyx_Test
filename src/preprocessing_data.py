import pandas as pd
from unidecode import unidecode
from datetime import datetime
from datetime import date
import calendar 

COLUMNS = ['cod_loc', 'idprovincia','iddepartamento', 'categoria', 
           'provincia','localidad', 'nombre',
           'direccion','cp','telefono','mail','web']

now = datetime.now()
today=date.today()
monthName = calendar.month_name[today.month]

def build_main_dataSet(dataframes):
    '''
    Concatenates the datasets to create the main dataset.
    Returns a DataFrame

    Params:

    dataframes = list: The three datasets (cinema, museums,libraries)

    '''
    pd_data = pd.concat(dataframes)
    pd_data['provincia'] = pd_data['provincia'].apply(unidecode) #Quit the accents
    pd_data['fecha'] = now # Add the 'fecha' column with actual Datetime
    return pd_data



def process_data(path):
    '''
    '''
    df2 = pd.read_csv(path)
    fix_data(df2)
    df2 = df2.filter(items=COLUMNS)  
    return df2

def fix_data(df2):
    '''
    '''
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
    
    category_df['fecha'] = now
    return category_df

def province_file(pd_data):
    province_df = pd_data[['provincia']]
    province_df = province_df.groupby(["provincia"])["provincia"].count()
    province_df = province_df.reset_index(name='cantidad')
    province_df['fecha'] = now
    return province_df

def cinema_file():
    file_path = f"files/cines/{today.year}-{monthName}/cines-{today}.csv"
    cinema_df = pd.read_csv(file_path)
    
    cinema_df = cinema_df.filter(items=['provincia','pantallas', 'butacas','espacio_incaa'])
    cinema_df['espacio_incaa'] = cinema_df['espacio_incaa'].replace(['Si','No'], [1,0])
    cinema_df = cinema_df.groupby(["provincia"]).sum()
    cinema_df=cinema_df.reset_index()
    cinema_df['fecha'] = now
    
    return cinema_df
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

def fix_data(path):
    '''
    Normalize the datasets columns and add missing columns

    Returns a normalized DataSet

    Params:
    path = String : Path of the csv file to process
    '''
    df = pd.read_csv(path) 
    df.columns = df.columns.str.lower() # Quit capital letters
    df.columns = [unidecode(col) for col in df.columns] #Quit Accents

    # Normalize columns names
    if 'domicilio' in df.columns:
        df.rename(columns = {'domicilio':'direccion'}, inplace = True)
    if 'cod_localidad' in df.columns:
        df.rename(columns = {'cod_localidad':'cod_loc'}, inplace = True)
    if 'id_provincia' in df.columns:
        df.rename(columns = {'id_provincia':'idprovincia'}, inplace = True)
    if 'id_departamento' in df.columns:
        df.rename(columns = {'id_departamento':'iddepartamento'}, inplace = True)
    
    # Add missing columns
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = None
    
    # Select the correct columns
    df = df.filter(items=COLUMNS)
    return df

def category_file(pd_data):
    '''
    Build the category dataframe to input in database
    Returns a DataFrame

    Params:

    pd_data = DataFrame : The main dataframe to extract the category column
    '''
    #Build the DataFrame
    category_df = pd.DataFrame({"Categoria":['Salas de cine',
                                     'Bibliotecas Populares',
                                     'Espacios de Exhibición Patrimonial'],
                        "Cantidad":[len(pd_data[pd_data['categoria']=='Salas de cine']),
                                    len(pd_data[pd_data['categoria']=='Bibliotecas Populares']),
                                    len(pd_data[pd_data['categoria']=='Espacios de Exhibición Patrimonial'])]})
    
    category_df['fecha'] = now # Add the 'fecha' column with actual Datetime

    return category_df

def province_file(pd_data):
    '''
    Build the province dataframe to input in database
    Returns a DataFrame

    Params:

    pd_data = DataFrame : The main dataframe to group by "provincia" column
    '''
    province_df = pd_data[['provincia']] #Select the "provincia" column
    province_df = province_df.groupby(["provincia"])["provincia"].count() #Count by province
    province_df = province_df.reset_index(name='cantidad') #Add "Cantidad" column
    province_df['fecha'] = now # Add the 'fecha' column with actual Datetime
    return province_df

def cinema_file():
    '''
    Build the cinema dataframe to input in database
    Returns a DataFrame
    '''
    file_path = f"files/cines/{today.year}-{monthName}/cines-{today}.csv" #Locate the cine file path
    cinema_df = pd.read_csv(file_path) #Build the dataframe
    
    cinema_df = cinema_df.filter(items=['provincia','pantallas', 'butacas','espacio_incaa']) #Select columns
    cinema_df['espacio_incaa'] = cinema_df['espacio_incaa'].replace(['Si','No'], [1,0]) #Replace bool to numbers
    cinema_df = cinema_df.groupby(["provincia"]).sum() # Group by "provincia" column to get sums of the other columns

    cinema_df=cinema_df.reset_index()
    
    cinema_df['fecha'] = now # Add the 'fecha' column with actual Datetime
    
    return cinema_df
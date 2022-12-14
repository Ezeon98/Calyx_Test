from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from src.logger import log

def create_tables(engine):
    '''
    Create the tables in the dataBase.
    The create_all method checks if the tables exists. If the tables exists, don't create new tables.


    '''
    meta=MetaData()

    # Design Tables
    Tcinema=Table(
    'cinema', meta, 
    Column('provincia', String), 
    Column('cantidad', Integer), 
    Column('fecha', DateTime)
        )
    
    Tcategory=Table(
    'category', meta, 
    Column('Categoria', String), 
    Column('cantidad', Integer), 
    Column('fecha', DateTime)
        )
    
    Tprovince=Table(
    'province', meta, 
    Column('provincia', String), 
    Column('cantidad', Integer), 
    Column('fecha', DateTime)
        )

    Tmain=Table(
    'main', meta, 
    Column('cod_loc', Integer), 
    Column('idprovincia', Integer),
    Column('iddepartamento', Integer), 
    Column('categoria', String),
    Column('provincia', String),
    Column('localidad', String),
    Column('nombre', String),
    Column('direccion', String),
    Column('cp', String),
    Column('telefono', String),
    Column('mail', String),
    Column('web', String),
    Column('fecha', DateTime)
        )

    try:
        meta.create_all(engine) #Create Tables
        log('Tables created Succeful', 'info')
    except Exception as ex:
        print(ex)
        log('Error in tables creation', 'error')
    return True
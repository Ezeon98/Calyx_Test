from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

def create_tables(engine):
    meta=MetaData()
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
    
    meta.create_all(engine)
    return True
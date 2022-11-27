from sqlalchemy import MetaData, Table, Column, Integer, String, text, create_engine


host='localhost'
user='postgres'
password='Calyx'
database='calyx'

def create_connection():
    engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
    return engine

# creates_tables(engine)

# inject_data(engine, 'cinema')

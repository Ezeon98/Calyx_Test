from sqlalchemy import MetaData, Table, Column, Integer, String, text, create_engine
from src.logger import log

host='localhost'
user='postgres'
password='Calyx'
database='calyx'

def create_connection():
    try:
        engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
    except Exception as ex:
        print(ex)
        log('Connection to DataBase Failed','error')
    return engine


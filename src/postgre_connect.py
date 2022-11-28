from sqlalchemy import create_engine
from src.logger import log
from decouple import config


host= config('DB_HOST')
user= config('DB_USER')
password= config('DB_PASSWORD')
database= config('DB_NAME')

def create_connection():
    '''
    Create connection to the DB. The credentials must have in .env file
    '''
    try:
        engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
    except Exception as ex:
        print(ex)
        log('Connection to DataBase Failed','error')
    return engine


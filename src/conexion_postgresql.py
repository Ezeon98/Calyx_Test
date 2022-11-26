from sqlalchemy import MetaData, Table, Column, Integer, String, text, create_engine
from create_tables_scripts import creates_tables


host='localhost'
user='postgres'
password='Calyx'
database='calyx'

engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")



creates_tables(engine)

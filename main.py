from src.postgre_connect import create_connection
from src.create_tables_scripts import create_tables
from src.inject_data import inject_data
from src.input_files import get_files

files=['main','cinema','province','category']

get_files()
# create_tables(create_connection())
for i in files:
    inject_data(create_connection(), i)

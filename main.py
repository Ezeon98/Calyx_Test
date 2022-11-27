from src.postgre_connect import create_connection
from src.create_tables_scripts import create_tables
from src.inject_data import inject_data
from src.download_files import get_files
from src.logger import log

files=['main','cinema','province','category']

get_files()
create_tables(create_connection())
for i in files:
    inject_data(create_connection(), i)
log('Script Finish', 'info')


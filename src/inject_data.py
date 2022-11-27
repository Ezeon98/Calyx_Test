import pandas as pd
from src.logger import log

path = 'mains_csv/'
def inject_data(engine, file):
    try:
        df = pd.read_csv(path + file +'.csv').to_sql(file, engine, if_exists='replace', index=False)
        log('Data Injected Succeful', 'info')
    except Exception as ex:
        print(ex)
        log('Error in Data Inject', 'error')

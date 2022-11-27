import pandas as pd
from src.logger import log

path = 'files/mains_csv/'
def inject_data(engine, file):
    try:
        df = pd.read_csv(path + file +'.csv').to_sql(file, engine, if_exists='replace', index=False)
    except Exception as ex:
        print(ex)
        log(f'Error in Data Inject. File: {file}', 'error')

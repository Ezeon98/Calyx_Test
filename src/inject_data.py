import pandas as pd

def inject_data(engine, file):
    path = 'files/mains_csv/'
    df = pd.read_csv(path + file +'.csv').to_sql(file, engine, if_exists='replace', index=False)
    # print(df)


# inject_data(1, 'cinema')
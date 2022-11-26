import pandas as pd



def inject_data(engine, file):
    path = 'mains_csv/'
    df = pd.read_csv(path + file +'.csv').to_sql('cinema', engine, if_exists=replace, index=False)
    print(df)


# inject_data(1, 'cinema')
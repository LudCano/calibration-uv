import pandas as pd
import datetime as dt
import os

## PROCESSING BREWER DATA FOR TUV RUNNING
o3_dir = 'data/BREWER_O3'
o3_files = sorted(os.listdir(o3_dir))
#the name of the file is the date, so we have to parse it
dfs = []
for file in o3_files:
    pth = os.path.join(o3_dir, file)
    date = file.split('-')[0]
    y,m,d = [int(i) for i in date.split('_')]
    df_ = pd.read_csv(pth, sep = '\s+')
    df_ = df_[['Type','Time','DS']]
    df_['datetime'] = pd.to_datetime(df_.Time, format = '%H:%M:%S')
    df_['datetime'] = [i.replace(year = y, month = m, day = d) - dt.timedelta(hours = 4) 
                       for i in df_.datetime]
    df_ = df_[df_.Type == 'ds'][['datetime','DS']]
    dfs.append(df_)

# concatenando df para o3
df = pd.concat(dfs, axis = 'rows').reset_index().drop('index', axis = 'columns')
d_0 = dt.datetime.strptime('2024-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')
d_f = dt.datetime.strptime('2024-11-15 13:00:00', '%Y-%m-%d %H:%M:%S')

# exportando
df = df[(df.datetime > d_0) & (df.datetime < d_f)].reset_index().drop('index', axis = 'columns')
df.columns = ['date','O3']
df.to_csv('outputs/brewer_O3_all.csv', index = False)

#obteniendo promedios diarios
df_daily = df.resample('1d', on = 'date').mean().reset_index()
df_daily['O3'] = df_daily['O3'].round(3)
df_daily.to_csv('outputs/brewer_O3_daily.csv', index = False)

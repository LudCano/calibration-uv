import pandas as pd

df = pd.read_csv('data/ambient_data.csv', parse_dates=["Simple Date"])
df = df[['Simple Date', 'Relative Pressure (hPa)', 'Outdoor Temperature (°C)', 'Solar Radiation (W/m^2)']]
df.columns = ['datetime','pressure','temperature','solar']
df = df.sort_values('datetime').reset_index().drop('index', axis = 1)
df.to_csv('outputs/ambient_all.csv', index=False)

df['temperature'] = df.temperature + 273.15
df['date'] = df.datetime.dt.date
df['hm'] = df.datetime.dt.hour + df.datetime.dt.minute/60

df = df[(df.hm >= 7) & (df.hm <= 18)]
df_ = df[['datetime','pressure','temperature']].resample('1d', on = 'datetime').mean().reset_index()
df_.columns = ['date','psurf','ztemp']

for c in ['date','psurf','ztemp']:
    df_[c] = round(df_[c], 3)

#print(df_)


#datos originales
comp = pd.read_csv('data/cimel_aod.csv', parse_dates=['date'])
comp['tauaer'] = round(comp.tauaer, 5)

#obteniendo O3 de outputs/O3_all
o3 = pd.read_csv('outputs/brewer_O3_daily.csv', parse_dates = ['date'])


#print(comp)
m = comp.merge(df_, on = 'date', how = 'inner')


m2 = m.merge(o3, on='date', how = 'inner')

m2.rename({'O3':'o3col'}, axis = 'columns', inplace=True)


m2.to_csv('outputs/tuv_pars.csv', index=False)
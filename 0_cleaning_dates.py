import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

instrs = ['yes138', 'yes139', 'yes140', 'tarija01', 'tarija02']
calib_w = [1.97, 2.07, 1.79, 1.79, 1.79]
calib_w = [0, 0, 0, 1.97, 1.79]


yes_pth = 'data/yes_data'
dfs = []
for f in os.listdir(yes_pth):
    pth = os.path.join(yes_pth, f)
    df_ = pd.read_csv(pth, skiprows=[0,2,3], parse_dates=['TIMESTAMP'])
    dfs.append(df_)

df = pd.concat(dfs, axis = 'rows')

# df = pd.read_csv('data/YES_LFA_minute1.dat', skiprows=[0,2,3], parse_dates=['TIMESTAMP'])
# #df.set_index('TIMESTAMP', inplace = True)

## LIMPIANDO FECHAS DEL NUEVO EXPERIMENTO
#d_0 = dt.datetime.strptime('2024-10-22 15:00:00', '%Y-%m-%d %H:%M:%S')
d_0 = dt.datetime.strptime('2024-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')
d_f = dt.datetime.strptime('2024-11-15 00:00:00', '%Y-%m-%d %H:%M:%S')

df = df[(df.TIMESTAMP >= d_0) & (df.TIMESTAMP < d_f)]

df2 = pd.read_csv('data/2024-11-20_yes_137x2.dat', skiprows=[0,2,3], parse_dates=['TIMESTAMP'])
df2 = df2[(df2.TIMESTAMP >= d_0) & (df2.TIMESTAMP < d_f)]
df2 = df2[['TIMESTAMP','YES_137']]
df2.rename({'YES_137':'yes137_Avg'}, axis = 'columns', inplace=True)


df = df.merge(df2, on = 'TIMESTAMP', how = 'outer')
df.sort_values('TIMESTAMP', inplace = True)
print(df)


# # PLOTTING
# fig, ax = plt.subplots()
# for i in instrs:
#     ax.scatter(df.TIMESTAMP, df[f'{i}_Avg'], label = i)
# ax.legend()
# plt.show()


# ## LIMPIANDO PAUSA
# d_0 = dt.datetime(2024,10,26,8,30)
# d_f = dt.datetime(2024,11,1,11,30)
# df = df[(df.TIMESTAMP <= d_0) | (df.TIMESTAMP >= d_f)]

# ## IGNORANDO YES139 hasta d_0
# df1 = df.copy()[df.TIMESTAMP <= d_0]
# df1.drop(['yes140_Avg', 'yes140_Std'], axis = 1, inplace=True)
# ## reemplazando yes140 con yes139 desde d_f
# df2 = df.copy()[df.TIMESTAMP >= d_f]
# df2 = df2.drop(['yes139_Avg','yes139_Std'], axis = 1).rename({'yes140_Avg':'yes139_Avg', 
#                                                               'yes140_Std':'yes139_Std'}, axis = 1)
# #concatenando
# df = pd.concat([df1,df2], axis = 0)

# PLOTTING
fig, ax = plt.subplots()
for i in instrs:
    ax.scatter(df.TIMESTAMP, df[f'{i}_Avg'], label = i)
ax.legend()
#plt.show()

df.to_csv('outputs/data_exp.csv', index = False)
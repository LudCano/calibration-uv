import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
## READING weighted values

import warnings
warnings.filterwarnings('ignore')

df0 = pd.read_csv('outputs/data_exp.csv', parse_dates=['TIMESTAMP'])
df0.sort_values('TIMESTAMP', inplace=True)
plot_series = True
night_start = 19
night_end   = 5

# Cortando para obtener solamente las noches
df = df0.copy()
df['hm'] = df.TIMESTAMP.dt.hour + df.TIMESTAMP.dt.minute/60
df = df[(df.hm >= night_start) | (df.hm <= night_end)]

dates = df.TIMESTAMP.dt.date.unique()
n_days = len(dates)


instruments = ['yes137','yes138','yes140','tarija01','tarija02']


## CORRELATION WITH Temp

from E_iterative_linear import iterative_linear

aw = pd.read_csv('outputs/ambient_all.csv', parse_dates=['datetime'])#ambient weather data
aw2 = aw.set_index('datetime').resample('1min').ffill()

## resampling
df_ = df.resample('5min',on = 'TIMESTAMP').mean().reset_index()
df_.rename({'TIMESTAMP':'datetime'}, axis='columns',inplace=True)
dfc = df0.copy().rename({'TIMESTAMP':'datetime'}, axis='columns')
m2 = dfc.merge(aw2, on = 'datetime', how = 'inner')
m2 = m2[['datetime','temperature'] + [f'{i}_Avg' for i in instruments] + [f'{i}_Std' for i in instruments[1:]]]

m = df_.merge(aw, on = 'datetime', how = 'inner')
m = m[['datetime','temperature'] + [f'{i}_Avg' for i in instruments] + [f'{i}_Std' for i in instruments[1:]]]
m['d_c'] = m.datetime.dt.day
m_ = m.dropna()
#fig, ax = plt.subplots(1,4)
fig2, axs2 = plt.subplots(5, 14, sharey='row', figsize = (20,8))
fig2.subplots_adjust(hspace = 0, wspace = 0)
for n,i in enumerate(instruments):
    #cma = ax[n].scatter(m.temperature, m[f'{i}_Avg'], c = m['d_c'], cmap = 'rainbow')
    if i!='yes137':
        res = iterative_linear(m_.temperature, m_[f'{i}_Avg'], 3, 1.5, 'WLS', m_[f'{i}_Std'])
    else:
        res = iterative_linear(m_.temperature, m_[f'{i}_Avg'], 3, 1.5, 'OLS')
    res.ax.set_title(i)
    res.fig.savefig(f'figures/{i}_temp_correction.png')
    #plt.show()
    f = open(f'outputs/iterative_temp_regressions/{i}_iterative_regression.txt', 'w')
    print(res.table, file = f)
    f.close()
    m2[f'{i}_Avg'] = m2[f'{i}_Avg'] - (m2.temperature*res.slope + res.intercept)
    #demostrando offset 0
    m3 = m_.copy()
    m3[f'{i}_Avg'] = m3[f'{i}_Avg'] - (m3.temperature*res.slope + res.intercept)
    m3['datetime'] = m3.datetime + dt.timedelta(hours = -6)
    for nday,day in enumerate(m3.datetime.dt.date.unique()):
        m3_ = m3.copy()[m3.datetime.dt.date == day]
        axs2[n,nday].scatter(m3_.datetime,m3_[f'{i}_Avg'])
        axs2[n,nday].set_ylim(-5,5)
        axs2[n,nday].xaxis.set_major_locator(mdates.HourLocator([14,18,22]))
        axs2[n,nday].xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        axs2[n,nday].set_xticklabels(['20','24','4'])
        axs2[n,nday].set_xlabel(dt.datetime.strftime(day, '%b%d'), fontsize = 14)
        axs2[n,0].set_ylabel(i)
    plt.close(res.fig)

fig2.supxlabel('Hora Local', fontsize = 18, y = 0.02)
fig2.supylabel('mV', x = 0.07, fontsize = 18)
fig2.suptitle('Offset corregido por temperatura', fontsize = 20, y = 0.95)
fig2.savefig('figures/offset_corregido_all.png')

m2.rename({'datetime':'TIMESTAMP'}, axis='columns',inplace=True)
m2.drop('temperature', axis = 'columns', inplace=True)
m2.to_csv('outputs/data_off2.csv', index = False)

#mostrando offset 0
#plt.show()
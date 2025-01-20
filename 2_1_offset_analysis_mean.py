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


## PLOTTING SERIES (figures/offset_series.png)
if plot_series:
    df_ = df.copy()
    df_['TIMESTAMP'] = df_.TIMESTAMP + dt.timedelta(hours = -6)
    #figure1: series
    fig, axs = plt.subplots(len(instruments),n_days, sharex=True, sharey='row',
                            figsize = (20,8))
    fig.subplots_adjust(hspace = 0, wspace = 0)
    dfs_all_instruments = []
    for y,i in enumerate(instruments):
        dfs = []
        if i!='yes137':
            dfc = df0.copy()[['TIMESTAMP',f'{i}_Avg',f'{i}_Std']]
        else:
            dfc = df0.copy()[['TIMESTAMP',f'{i}_Avg']]
        for x,d in enumerate(dates):
            df__ = df_[df_.TIMESTAMP.dt.date == d]
            dfday = dfc[(dfc.TIMESTAMP.dt.date == d)]
            df__['TIMESTAMP'] = [i.replace(month = 11, day = 1) for i in df__['TIMESTAMP']]
            axs[y][x].scatter(df__.TIMESTAMP, df__[f'{i}_Avg'], c = 'k', s = 3)
            offset_thisday = df__[f'{i}_Avg'].median()
            axs[y][x].axhline(offset_thisday, c ='r', ls = '--', lw = 3) 
            dfday[f'{i}_Avg'] = dfday[f'{i}_Avg'] - offset_thisday
            dfday = dfday.reset_index().drop('index', axis = 'columns')
            dfs.append(dfday)
            axs[y][x].xaxis.set_major_locator(mdates.HourLocator(interval=4))
            axs[y][x].xaxis.set_major_formatter(mdates.DateFormatter('%H'))
            axs[-1][x].set_xlabel(dt.datetime.strftime(d, '%b%d'), fontsize = 14)
            axs[y][x].set_xticklabels(['19','23','3'])
            axs[y][x].grid(alpha=0.3)
        axs[y][0].set_ylabel(i, fontsize = 14)
        df_instrument = pd.concat(dfs, axis = 'rows')
        tms = df_instrument.TIMESTAMP
        df_instrument.drop('TIMESTAMP', axis = 'columns', inplace = True)
        dfs_all_instruments.append(df_instrument)
    df_corrected = pd.concat(dfs_all_instruments, axis = 'columns')
    
    df_corrected['TIMESTAMP'] = tms

    df_corrected = df_corrected[['TIMESTAMP'] + list(df_corrected.columns)[:-1]]

    fig.supxlabel('Hora Local', fontsize = 18, y = 0.02)
    fig.supylabel('mV', x = 0.07, fontsize = 18)
    fig.savefig('figures/offset_series.png', dpi = 300)
    plt.show()
print(df_corrected)

df_corrected.to_csv('outputs/data_off1.csv', index=False)



import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
#import scienceplots
import numpy as np
#plt.style.use(['science', 'nature'])

tuv = pd.read_csv('outputs/tuv_minute.csv', parse_dates = ['datetime'])
brew = pd.read_csv('outputs/brewer_UVB_all.csv', parse_dates = ['datetime'])
yes = [pd.read_csv(f'outputs/weighted_off{i}.csv', parse_dates = ['TIMESTAMP']) for i in range(3)]
yes = [i.rename({'TIMESTAMP':'datetime'}, axis = 'columns') for i in yes]
#print(yes[0])
#print(yes_merged[0].columns)
instruments = ['yes137','yes138','yes140','tarija01','tarija02']

threshold = 0.5

#eliminando nubes
for offset in range(1):
    m_ = tuv.merge(yes[offset], on = 'datetime', how = 'inner')
    for i in instruments:
        m_[f'dif_{i}'] = m_.uvb - m_[f'{i}_uvb']

        # generando tamaño del plot
    dates = m_.datetime.dt.date.unique()
    n_days = len(dates)
    n_rows = 4
    if (n_days/n_rows) > (n_days//n_rows):
        print('wuu')
        n_cols = n_days//n_rows + 1
    else:
        n_cols = n_days//n_rows

    # genearndo figura
    fig, ax = plt.subplots(n_rows, n_cols, sharex=True, sharey = True, figsize=(16,9))
    fig.subplots_adjust(hspace = 0.1, wspace= 0.1)
    axs = ax.flatten()
    dates = sorted(dates)
    for n, date in enumerate(dates):
        df_d = m_[m_.datetime.dt.date == date].copy()
        df_d['hm'] = df_d.datetime.dt.hour + df_d.datetime.dt.minute/60
        df_d.sort_values('hm', inplace=True)
        lns = []
        for i in instruments:
            line, = axs[n].plot(df_d.hm, df_d[f'dif_{i}']**2, label = i)
            lns.append(line)
        axs[n].annotate(dt.datetime.strftime(date,'%d%b'), (0.1,0.9), xycoords = 'axes fraction')
        axs[n].axhline(threshold, c = 'k', alpha = 0.3, ls = '--')
        axs[n].grid(alpha = 0.3, ls = '--')
    for k in axs[-n_cols:]:
        k.set_xticks(np.arange(6,19,2))

    fig.supxlabel('Hora Local', y = 0.05, fontsize = 15)
    fig.supylabel('(TUV - Instrument)^2', x = 0.07, fontsize = 15)
    fig.suptitle(f'Filter for clouds offset {offset}', fontsize = 17, y = 0.92)
    fig.legend(handles = lns, loc = 'center right')
    fig.savefig(f'figures/calendar_cleaning_clouds_off{offset}.png', dpi = 300)

    #cleaning
    for i in instruments:
        m_ = m_[m_[f'dif_{i}']**2 <= threshold]
    m_.to_csv(f'outputs/noclouds_off{offset}.csv', index = False)


plt.show()
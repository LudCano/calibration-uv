import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

instrs = ['yes137','yes138', 'yes140', 'tarija01', 'tarija02']

tuv = pd.read_csv('data/TUV_concatenated.csv', parse_dates = ['datetime'])
brew = pd.read_csv('outputs/brewer_UVB_all.csv', parse_dates = ['datetime'])

for o in range(3):
    df = pd.read_csv(f'outputs/weighted_off{o}.csv', parse_dates = ['TIMESTAMP'])

    # generando tamaño del plot
    dates = df.TIMESTAMP.dt.date.unique()
    n_days = len(dates)
    n_rows = 4
    if (n_days/n_rows) > (n_days//n_rows):
        print('wuu')
        n_cols = n_days//n_rows + 1
    else:
        n_cols = n_days//n_rows

    #filtrando horas
    h_start = 6; h_end = 18
    df_ = df[(df.TIMESTAMP.dt.hour >= h_start) & (df.TIMESTAMP.dt.hour < h_end)]
    tuv = tuv[(tuv.datetime.dt.hour >= h_start) & (tuv.datetime.dt.hour < h_end)]
    brew = brew[(brew.datetime.dt.hour >= h_start) & (brew.datetime.dt.hour < h_end)]

    # genearndo figura
    fig, ax = plt.subplots(n_rows, n_cols, sharex=True, sharey = True, figsize=(16,9))
    fig.subplots_adjust(hspace = 0.1, wspace= 0.1)
    axs = ax.flatten()
    dates = sorted(dates)
    for n, date in enumerate(dates):
        df_d = df_[df_.TIMESTAMP.dt.date == date].copy()
        df_d['hm'] = df_d.TIMESTAMP.dt.hour + df_d.TIMESTAMP.dt.minute/60
        df_d.sort_values('hm', inplace=True)
        tuv_d = tuv[tuv.datetime.dt.date == date]
        tuv_d['hm'] = tuv_d.datetime.dt.hour + tuv_d.datetime.dt.minute/60
        brew_d = brew[brew.datetime.dt.date == date]
        brew_d['hm'] = brew_d.datetime.dt.hour + brew_d.datetime.dt.minute/60
        tuv_line,= axs[n].plot(tuv_d.hm, tuv_d.uvb, label = 'TUV', c = 'dimgray', lw =2, ls = '--')
        brew_line, = axs[n].plot(brew_d.hm, brew_d.UVB, label = 'Brewer', c = 'k', lw = 2)
        lns = []
        for i in instrs:
            line, = axs[n].plot(df_d.hm, df_d[f'{i}_uvb'], label = i)
            lns.append(line)
        axs[n].annotate(dt.datetime.strftime(date,'%d%b'), (0.1,0.9), xycoords = 'axes fraction')
        axs[n].grid(alpha = 0.3, ls = '--')
    lns.append(tuv_line)
    lns.append(brew_line)
    for k in axs[-n_cols:]:
        k.set_xticks(np.arange(6,19,2))

    fig.supxlabel('Hora Local', y = 0.05, fontsize = 15)
    fig.supylabel('UVB', x = 0.07, fontsize = 15)
    fig.legend(handles = lns, loc = 'center right')
    fig.savefig(f'figures/calendar_allinstrs_off{o}.png', dpi = 400)

plt.show()

# genearndo figura
# fig, ax = plt.subplots(n_rows, n_cols, sharex=True, sharey = True, figsize=(16,9))
# fig.subplots_adjust(hspace = 0.1, wspace= 0.1)
# axs = ax.flatten()
# dates = sorted(dates)
# for n, date in enumerate(dates):
#     df_d = df_[df_.TIMESTAMP.dt.date == date].copy()
#     df_d['hm'] = df_d.TIMESTAMP.dt.hour + df_d.TIMESTAMP.dt.minute/60
#     df_d.sort_values('hm', inplace=True)
#     lns = []
#     for i in instrs:
#         line, = axs[n].plot(df_d.hm, df_d[f'{i}_ery']*1000, label = i)
#         lns.append(line)
#     axs[n].annotate(dt.datetime.strftime(date,'%d%b'), (0.1,0.9), xycoords = 'axes fraction')
#     axs[n].grid(alpha = 0.3, ls = '--')

# for k in axs[-n_cols:]:
#     k.set_xticks(np.arange(6,19,2))

# fig.supxlabel('Hora Local', y = 0.05, fontsize = 15)
# fig.supylabel('Erythema (mW/m^2)', x = 0.07, fontsize = 15)
# fig.legend(handles = lns, loc = 'center right')
# fig.savefig('figures/calendar_physical_ery.png', dpi = 400)
# plt.show()
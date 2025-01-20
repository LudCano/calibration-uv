import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

df = pd.read_csv('outputs/data_exp.csv', parse_dates = ['TIMESTAMP'])
instrs = ['yes137','yes138', 'yes140', 'tarija01', 'tarija02']

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


# genearndo figura
fig, ax = plt.subplots(n_rows, n_cols, sharex=True, sharey = True, figsize=(16,9))
fig.subplots_adjust(hspace = 0.1, wspace= 0.1)
axs = ax.flatten()
for n, date in enumerate(sorted(dates)):
    df_d = df_[df_.TIMESTAMP.dt.date == date].copy()
    df_d['hm'] = df_d.TIMESTAMP.dt.hour + df_d.TIMESTAMP.dt.minute/60
    df_d.sort_values('hm', inplace = True)
    #df_d = df_d[(df_d.hm >= 14) & ( df_d.hm <= 17)]
    lns = []
    for i in instrs:
        line, = axs[n].plot(df_d.hm, df_d[f'{i}_Avg'], label = i)
        lns.append(line)
    axs[n].annotate(dt.datetime.strftime(date,'%d%b'), (0.1,0.9), xycoords = 'axes fraction')
    axs[n].grid(alpha = 0.3, ls = '--')

for k in axs[-n_cols:]:
    k.set_xticks(np.arange(6,19,2))

fig.supxlabel('Hora Local', y = 0.05, fontsize = 15)
fig.supylabel('mV', x = 0.07, fontsize = 15)
fig.legend(handles = lns, loc = 'center right')
fig.savefig('figures/calendar_raw.png', dpi = 400)
plt.show()
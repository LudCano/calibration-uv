import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import scienceplots
from E_iterative_linear import iterative_linear
plt.style.use(['science', 'nature'])

tuv = pd.read_csv('data/TUV_concatenated.csv', parse_dates = ['datetime'])
brew = pd.read_csv('outputs/brewer_UVB_all.csv', parse_dates = ['datetime'])
yes = [pd.read_csv(f'outputs/weighted_off{i}.csv', parse_dates = ['TIMESTAMP']) for i in range(3)]

#resampling del yes, usando el valor promedio de 2 a 32
yes_sample = [i[(i.TIMESTAMP.dt.minute == 2) | (i.TIMESTAMP.dt.minute == 32)] 
              for i in yes]

yes_merged = [i.merge(brew, right_on = 'datetime', left_on = 'TIMESTAMP', how = 'right')
              for i in yes_sample]

#print(yes_merged[0].columns)
instruments = ['yes137','yes138','yes140','tarija01','tarija02']

for k in range(3):
    fig,axss = plt.subplots(2,5, figsize=(16,5), sharex=True, sharey='row',
                            height_ratios=[3,1], dpi = 120)
    #fig.tight_layout()
    #axss = axs.flatten()
    #print(f'OFFSET {k}')
    fig.subplots_adjust(wspace=0.05, hspace=0.03, left = 0.05, right = 0.97)
    for n,i in enumerate(instruments):
        yes_merged_ = yes_merged[k].dropna()
        #print(len(yes_merged[k]), len(yes_merged_))
        x = yes_merged_.UVB
        y = yes_merged_[f'{i}_uvb']
        model = iterative_linear(x, y, 3, 2)
        #print(i, r2, m, b)
        axss[0,n].scatter(x, y, c = 'k', s = 3)
        axss[0,n].set_title(i, fontsize = 13)
        axss[0,n].plot(x, model.slope*x + model.intercept, c = 'r')
        axss[0,n].annotate(f'R2 = {round(model.r2,3)}', (0.1, 0.85), xycoords = 'axes fraction', fontsize = 13)
        axss[0,n].annotate(f'{round(model.slope,2)}x + {round(model.intercept,2)}', (0.1, 0.9), xycoords = 'axes fraction', fontsize = 13)
        axss[0,0].set_ylabel('Instrument UVB [W/m2]', fontsize = 12)
        axss[1,n].scatter(x, model.slope*x + model.intercept - y, s = 3, c = 'k')
        axss[1,n].axhline(0, c = 'k', lw = 1, alpha = .3)
        axss[1,0].set_ylabel('Residual [W/m2]', fontsize = 12)
        axss[1,n].tick_params(axis='both', labelsize=12)
    fig.supxlabel('Brewer UVB [W/m2]', y = 0.015, fontsize = 12)
    fig.suptitle(f'Correlation - Offset {k} w/ clouds', fontsize = 16)
    #     print(i)
    #     print(model.table)
    fig.savefig(f'figures/correlation_brewer_wclouds_off{k}.png', dpi = 300)
#plt.show()

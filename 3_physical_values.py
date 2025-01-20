### GETTING PHYSICAL VALUES
import pandas as pd
from A_get_weights2 import get_weights

instrs = ['yes138', 'yes139', 'tarija01', 'tarija02']
calib_w = [1.97, 2.07, 1.79, 1.79]
#calib_w = [0, 0, 0, 1.97, 1.79]


instrs = ['yes137','yes138', 'yes140', 'tarija01', 'tarija02']
calib_w = [1.97,1.97, 1.79, 1.79, 1.79]

for off in range(3):

    df = pd.read_csv(f'outputs/data_off{off}.csv')
    df0 = df.copy()
    df_w = get_weights(df0, 'TIMESTAMP')

    print(df_w.columns)

    for i, w in zip(instrs, calib_w):
        df_w.loc[:,f'{i}_uvb'] = df_w['uvb320_w']*df_w[f'{i}_Avg']*w/1000
        if i!='yes137':
            df_w.loc[:,f'{i}_uvb_std'] = df_w['uvb320_w']*df_w[f'{i}_Std']*w/1000
        #df_w.loc[:,f'{i}_ery'] = df_w['uvb320_w']*df_w[f'{i}_Avg']*w*df_w['parrish_w']/1000

    df_w.sort_values('TIMESTAMP', inplace=True)
    df_w.to_csv(f'outputs/weighted_off{off}_allcols.csv', index=False)

    # df_clean = df_w[['TIMESTAMP'] + [f'{i}_Avg' for i in instrs] + 
    #                 [f'{i}_uvb' for i in instrs] + [f'{i}_ery' for i in instrs]]
    # df_clean = df_w[['TIMESTAMP'] + [f'{i}_Avg' for i in instrs] + 
    #                 [f'{i}_uvb' for i in instrs] + [f'{i}_uvb_std' for i in instrs]]
    df_clean = df_w[['TIMESTAMP'] + 
                    [f'{i}_uvb' for i in instrs] + [f'{i}_uvb_std' for i in instrs[1:]]]


    df_clean.to_csv(f'outputs/weighted_off{off}.csv', index=False)

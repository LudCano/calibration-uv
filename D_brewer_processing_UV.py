import pandas as pd
import datetime as dt

# uva_pth = 'data/BREWER_UV/UVA_non_weighted_2009_to_2024.txt'
# uvb_pth = 'data/BREWER_UV/UVB_non_weighted_2009_to_2024.txt'

uva_pth = 'data/BREWER_UV/2024_11_21_UVA.txt'
uvb_pth = 'data/BREWER_UV/2024_11_21_UVB.txt'


def read_ifile(pth):
    uva = pd.read_csv(pth, sep = '\s+', header = None)
    name = pth.split('/')[-1].split('_')[-1].split('.')[0]
    uva.columns = ['date','time','za','temp','uv']
    uva['datetime'] = pd.to_datetime(uva.date +' '+ uva.time, 
                                     format = '%d.%m.%Y %H:%M:%S') - dt.timedelta(hours = 4, seconds = 10)#, minutes = 2, seconds=10)
    uva['uv'] = uva.uv/1000
    uva = uva[['datetime','uv']]
    uva = uva[(uva.datetime >= dt.datetime(2024,11,1)) & (uva.datetime < dt.datetime(2024,11,15))]
    uv_exp = uva.copy().rename({'uv':name}, axis = 'columns')
    uv_exp.to_csv(f'outputs/brewer_{name}_all.csv', index = False)
    return uva

uva = read_ifile(uva_pth)
uvb = read_ifile(uvb_pth)

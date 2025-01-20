import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt


def linear(x,y,method = 'OLS', weights = None):
    X = sm.add_constant(x)
    Y = y
    if method == 'OLS':
        model_ = sm.OLS(Y, X).fit()
    elif method == 'WLS':
        model_ = sm.WLS(Y, X, weights=weights).fit()
    b, m = model_.params
    p = x*m + b
    r2 = model_.rsquared
    return m, b, p, r2


# def iterative_linear(x,y,n_steps,threshold=1.5,method = 'OLS', weights = None, show_plt = False,
#                      print_pars = True):
#     plt.figure()
#     x2 = x; y2 = y; w2 = weights; p2 = y
#     if print_pars:
#         print('     Slope  Intercept         R2     n_data     dif_n_data')
#     for i in range(n_steps):
#         if method == 'WLS':
#             m,b,p,r2 = linear(x2,y2, weights=w2)
#         elif method == 'OLS':
#             m,b,p,r2 = linear(x2,y2)
#         residuals = y2 - p
#         desvest = np.std(residuals)
#         l0 = len(x2)
#         x_ = x2
#         x2 = x2[abs(residuals) < threshold*desvest]
#         y2 = y2[abs(residuals) < threshold*desvest]
#         if len(weights) > 0:
#             w2 = w2[abs(residuals) < threshold*desvest]
#         p2 = p2[abs(residuals) < threshold*desvest]
#         #n_t = l0 - len(x2)
#         plt.plot(x_, p, label = i+1)
#         if print_pars:
#             #print(m,b,round(r2, 3), len(x2), len(x2)-l0)
#             print(f'{m: 10.4f} {b: 10.4f} {r2: 10.3f} {len(x2): 10} {len(x2)-l0: 14}')
    
#     plt.scatter(x, y)
#     plt.scatter(x2, y2)
#     plt.legend()
#     if show_plt:
#         plt.show()

#     return m,b,r2


class iterative_linear:
    def __init__(self,x,y,n_steps,threshold=1.5,method = 'OLS', weights = None,
                     print_pars = True):
        x2 = x; y2 = y; w2 = weights; p2 = y
        header = '     Slope  Intercept         R2     n_data     dif_n_data'
        ms = []; bs = []; r2s = []
        for i in range(n_steps):
            if method == 'WLS':
                m,b,p,r2 = linear(x2,y2, weights=w2)
            elif method == 'OLS':
                m,b,p,r2 = linear(x2,y2)
            ms.append(m)
            bs.append(b)
            r2s.append(r2)
            residuals = y2 - p
            desvest = np.std(residuals)
            l0 = len(x2)
            x_ = x2
            x2 = x2[abs(residuals) < threshold*desvest]
            y2 = y2[abs(residuals) < threshold*desvest]
            if method=='WLS':
                w2 = w2[abs(residuals) < threshold*desvest]
            p2 = p2[abs(residuals) < threshold*desvest]
            #n_t = l0 - len(x2)
            #plt.plot(x_, p, label = i+1)
            lin = f'{m: 10.4f} {b: 10.4f} {r2: 10.3f} {len(x2): 10} {len(x2)-l0: 14}'
            header = header + '\n' + lin
            
        self.xend = x2
        self.yend = y2
        self.x0 = x
        self.y0 = y
        self.table = header
        self.slope = m
        self.intercept = b
        self.r2 = r2
        self.all_slopes = ms
        self.all_intercepts = bs
        self.all_coeff = r2s
        fig, ax = plt.subplots()

        ax.scatter(self.x0, self.y0)
        ax.scatter(self.xend, self.yend)
        ax.legend()

        self.fig = fig
        self.ax  = ax
    def show_plot(self):
        
        plt.show()

    def print_table(self):
        
        print(self.table)



if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv('test.csv')
    df = df.dropna()
    x = df.temperature
    y = df.tarija02_uvb
    w = df.tarija02_uvb_std
    #m,b,p,r2 = linear(x,y, weights=w)

    aa = iterative_linear(x,y,7,2,'WLS',w)
    # plt.figure()
    # plt.hist(df.res)
    # plt.show()
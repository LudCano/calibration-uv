from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def fit_poly(xfit, yfit, xtofit = [], deg = 6):
    X = xfit.values.reshape(-1,1)
        
    pr = PolynomialFeatures(degree = deg)
    X_poly = pr.fit_transform(X)
    lr_2 = LinearRegression()
    lr_2.fit(X_poly, yfit)

    pred_1 = lr_2.predict(X_poly)  # Polynomial Regression

    if len(xtofit) > 0:
        x2 = xtofit.values.reshape(-1,1)
        X_poly2 = pr.fit_transform(x2)
        pred_2 = lr_2.predict(X_poly2)
    else:
        pred_2 = None

    return pred_1, pred_2



if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt

    tuv = pd.read_csv('data/TUV_concatenated.csv', parse_dates = ['datetime'])
    tuv['hm'] = tuv.datetime.dt.hour + tuv.datetime.dt.minute/60 + tuv.datetime.dt.second/3600
    dfs = []
    for day in tuv.datetime.dt.date.unique():
        tuv_ = tuv[tuv.datetime.dt.date == day]
        ranges = pd.date_range(day, freq='1min', periods=1440)
        ranges = ranges.to_series()
        ranges = ranges[(ranges.dt.hour >= 7) & (ranges.dt.hour <= 17)]
        rangeshm = ranges.dt.hour + ranges.dt.minute/60 + ranges.dt.second/3600
        p1, p2 = fit_poly(tuv_.hm, tuv_.uvb, rangeshm)
        df = pd.DataFrame(list(zip(ranges, p2)), columns=['datetime','uvb'])
        dfs.append(df)
    dff = pd.concat(dfs, axis='rows')
    dff.to_csv('outputs/tuv_minute.csv', index = False)

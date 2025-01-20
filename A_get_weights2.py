from pvlib import solarposition
import datetime as dt
import pandas as pd
import numpy as np


def get_weights(df, col_dt = 'fecha_hora'):
    """Gets the weights for a general pandas Dataframe

    Args:
        df (pd.DataFrame): a dataframe that has a column with a datetime-like column.
        col_dt (str, optional): name of the column containing the datetime-like column. Defaults to 'fecha_hora'.

    Returns:
        df_weights: Same dataframe but with 3 new columns: sza for the solar zenith angle, uvb_w for uvb weights and diffey_w for the Diffey weight
    """
    print('Calculating the solar position and weights...')
    dates = df[col_dt]
    
    # Adding 4 hours because of the timezone
    dates = pd.to_datetime(dates) + dt.timedelta(hours = 4)

    # Getting the solar zenith angle
    a = solarposition.get_solarposition(time = dates, latitude = -16.538986, longitude = -68.066475)
    ## In the next line, change for 1 if you want the solar zenith angle instead of the apparent
    a = a.iloc[:,[0]]
    a.reset_index(inplace = True)
    a.columns = [col_dt, 'sza']
    # Substracting the 4 hours to get the desired output
    a[col_dt] = a[col_dt] + dt.timedelta(hours = -4)

    d2 = pd.read_csv('data/calib_constants.csv')

    def get_weights(sza):
        """Gets the weights with the closest sza available

        Args:
            sza (pd.Series): a Pandas Series that contains solar zenith angles

        Returns:
            weights: pd.Series with the weights calculated
        """
        idx = np.argmin(abs(sza - np.array(d2.sza)))
        uvb315 = d2.uvb315.to_list()[idx]
        uvb320 = d2.uvb320.to_list()[idx]
        dif = d2.diffey.to_list()[idx]
        par = d2.parrish.to_list()[idx]
        rw = {'uvb315_w': uvb315,'uvb320_w': uvb320, 'diffey_w': dif, 'parrish_w': par}
        return pd.Series(rw)

    r = a.sza.apply(get_weights)
    df.reset_index(inplace = True)
    col0 = list(df.columns) + list(r.columns)
    df_weights = pd.concat([df, r], axis = 'columns', ignore_index=True)
    df_weights.columns = col0
    df_weights.drop('index', axis = 1, inplace = True)
    #sprint(df_weights)

    return df_weights



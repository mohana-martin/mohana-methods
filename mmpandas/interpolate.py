# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:02:31 2021

@author: mohanam
"""

import pandas as pd
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression

def resample_DF(df, freq="1H", window=7):
    """Resample, interpolate and smoothen with savgol_filtering

    Interpolation using splines does not work well with pandas DataFrames and 
    produces inconsistent data. This 

    Parameters
    ----------
    df : pandas DataFrame
    freq : str
        see pandas.DataFrame.resample argument "rule"
        Default True.
    window : int
        see scipy.signal.savgol_filter argument "window_length". Should be 
        odd. The larger, the more smoothing is applied.
        Default 7.

    Returns
    -------
    pandas DataFrame
    """
    df = df.resample(freq).asfreq()
    
    for iColumn in df.columns:
        df[iColumn] = savgol_filter(df[iColumn].interpolate(), 
                                    window_length=window,
                                    deriv=0,
                                    polyorder=1)
    return df

def linreg(df, tagX, tagY, **kwargs):
    """Quick linear regression model.

    Parameters
    ----------
    df : pandas DataFrame
    tagX : str
        string specifying the column of the df to take X values from.
    tagY : str
        string specifying the column of the df to take Y values from.
    fit_intercept : bool
        Default=True

    Returns
    -------
    sklearn.linear_model._base.LinearRegression
    """
    linear_regression = LinearRegression(**kwargs)
    
    X = df[tagX].values.reshape(-1, 1)
    Y = df[tagY].values.reshape(-1, 1)
    
    return linear_regression.fit(X, Y)
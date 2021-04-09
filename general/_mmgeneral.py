# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 17:08:45 2021

@author: mohanam
"""

def limit(v, minmax):
    """Limit a certain variable between a range.
    
    Range is taken from minmax by applying min() and max().

    Parameters
    ----------
    v : int or float
        the variable to be limited
    minmax: list, tuple, set, pandas Series, pandas DataFrame, etc.
        anything that is accepted by min(), max()
    
    Returns
    -------
    int or float
        the variable limited by the range
    """
    return max(min(minmax),min(max(minmax),v))

def find_nearest(array, value):
    """Find the nearest array value to a given value.
    
    Looks for the closest value in an array to a given value.

    Parameters
    ----------
    array : list-like
        array to search for the closest value
    value: int or float
        the value
    
    Returns
    -------
    int or float
        the value closest to the value in the array
    """
    n = [abs(i-value) for i in array]
    idx = n.index(min(n))
    return array[idx]
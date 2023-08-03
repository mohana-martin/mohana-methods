# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:36:47 2021

@author: mohanam
"""

from copy import deepcopy as dc
import json
import numpy as np

def denumpy(d, deepcopy=False):
    """Converts numpy variables to python variables in a nesteed structure.

    A recursive function that traverses through a nested dictionary or 
    list-like structure and converts numpy objects (such as ndarray or int64)
    to python objects (such as list or int). 
    
    By default it will overwrite the original dictionary.
    
    Types that it does not recognize, it ignores.
    
    Parameters
    ----------
    d : dict or list-like
    deepcopy : bool
        Default False
    
    Returns
    -------
    dict or list-like
        with converted values.
    """
    if deepcopy:
        d = dc(d)
    if type(d) is dict:
        trav = list(d.keys())
    elif type(d) is list:
        trav = range(len(d))
    for i in trav:
        if type(d[i]) in [list, np.ndarray]:
            d[i] = list(d[i])
            denumpy(d[i])
        if type(d[i])==dict:
            denumpy(d[i])
        if type(d[i]) in [np.int16,np.int32,np.int64]:
            d[i] = int(d[i])
        if type(d[i]) in [np.float16,np.float32,np.float64]:
            d[i] = float(d[i])
    return d

def open_json(file_dir):
    with open(file_dir) as file:  
        data = json.load(file)
    return data

def save_json(dictionary, file_dir):
    with open(file_dir, 'w') as file:  
        json.dump(dictionary, file)
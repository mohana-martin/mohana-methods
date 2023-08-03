# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:22:37 2020

@author: mohanam
"""

import os
import glob
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
from scipy.signal import savgol_coeffs

def importLog(fileDir, units = False):
    r"""Import data from the Carya log file.

        Arguments
        ---------
        FileDir : str
            path to the Carya log file
            
        Units : bool
            whether to 
        

        Returns
        -------
        pandas.DataFrame
            with all the data from the log file
    """
    # Get the file name from the directory
    FileName = fileDir.split(os.sep)[-1]
    # Import the file
    print(f"Importing {FileName}")
    retDF = pd.read_csv(fileDir, 
                            skiprows=[1], 
                            delimiter="\t", 
                            index_col=0, 
                            parse_dates=True, 
                            on_bad_lines="warn", 
                            encoding = "ISO-8859-15")
    # Convert it into a datetime object in order to be able to select data out
    # and make plotly x axis
    retDF.index = pd.to_datetime(retDF.index)
    print("Imported!")
    if not units:
        return retDF       
    else:
        print(f"Importing units from {FileName}")
        Units = pd.read_csv(fileDir, 
                            header=[0], 
                            delimiter="\t", 
                            index_col=0, 
                            nrows=1, 
                            encoding = "ISO-8859-15")
        retUnits = Units.loc['System'].to_dict()
        print("Imported!")   
        return retDF, retUnits

def importLogs(listFileDir):
    r"""Import and concat data from the Carya log files.
    Assumes all log files to have same units.
     
    Arguments
    ---------
        listFileDir : list
            list of paths to the Carya log file
    
    
    
    Returns
    -------
        pandas.DataFrame
            with all the data from the log file
    
    """
    ret = []
    for iFileDir in listFileDir:
        ret.append(importLog(fileDir=iFileDir, units=False))
    retDF = pd.concat(ret)
    return retDF

def exportData(df, fileDir):
    r"""Exports and concat data from the Carya log files.
    Assumes all log files to have same units.


    """
    print(f"Exporting to {fileDir}")
    if len(fileDir.split(".")) == 1:
        print("Assuming file type .csv")
        fileDir += ".csv"
    df.to_csv(fileDir)
    print("Exported!")
    
def importData(fileDir):
    r"""


    """
    return pd.read_csv(fileDir, index_col=0, parse_dates=True)
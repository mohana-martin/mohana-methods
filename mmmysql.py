# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:38:08 2021

@author: mohanam
"""

import mysql.connector
import pandas as pd


class Carya_DB_Handler(object):
    
    def __init__(self,
                 passwd,
                 database,
                 host="localhost",
                 user="root"):
    
        self._database = database
        self._dbconnector = mysql.connector.connect(host=host,
                                                   user=user,
                                                   passwd=passwd,
                                                   database=database)
        
    def _queryTables(self):
        """Gets all the tables from the database.
    
        Convinience function to obtain all the tables from the MySQL Database.
    
        Returns
        -------
        list of tuples contianing information about the respective tables
        """
        self._dbconnector.commit()
        mycursor = self._dbconnector.cursor()
        mycursor.execute("SHOW TABLE STATUS")    
        tables = [iTable for iTable in mycursor]
        mycursor.close()
        return tables
    
    @staticmethod
    def _selectLatestTable(Tables):
        """Returns the latest table name in the MySQL database.
    
        Returns
        -------
        str
        """
        TablesTimes = [table[11] for table in Tables if table[11] is not None and 'inter' not in table[0]]
        TablesNames = [table[0] for table in Tables if table[11] is not None and 'inter' not in table[0]]
        Newest_index = TablesTimes.index(max(TablesTimes))
        Newest_name = TablesNames[Newest_index]
        return Newest_name

    @staticmethod
    def _cleanHeaders(df):
        mapper={}
        for i in df:
            mapper[i]=i.split("[")[0]
        return df.rename(columns=mapper)
    
    def queryData_All(self, table_name="", every=1, clean=False):
        """Returns all of the data in a certian table in the MySQL database.
    
        By default it takes the latest table and every datapoint
        
        Returns
        -------
        pandas.DataFrame
        """
        if not(table_name):
            table_name = self.latest_table
        self._dbconnector.commit()
        df = pd.read_sql(f"SELECT * FROM `{self._database}`.`{table_name}` WHERE ID mod {every}= 0", 
                         self._dbconnector, 
                         index_col = "TimeStamp[System]").drop("id",axis=1)
        if clean:
            df = self._cleanHeaders(df)
        return df
    

    def queryData_From(self, table_name="", row=0, every=1, clean=False):
        """Returns all of the data from a certian table from a certain row ID in the MySQL database.
    
        By default it takes the latest table and every row since the first row.
        
        Returns
        -------
        pandas.DataFrame
        """
        if not(table_name):
            table_name = self.latest_table
        self._dbconnector.commit()
        df = pd.read_sql(f"SELECT * FROM `{self._database}`.`{table_name}` WHERE ID > {row} AND ID mod {every} = 0", 
                         self._dbconnector, 
                         index_col = "TimeStamp[System]").drop("id",axis=1)
        if clean:
            df = self._cleanHeaders(df)
        return df

    def queryData_Last(self, table_name="", rows=1, every=1, clean=False):
        """Returns the last rows of a certian table in the MySQL database.
    
        By default it takes the latest table and last row since the first row.
        
        Returns
        -------
        pandas.DataFrame
        """
        if not(table_name):
            table_name = self.latest_table
        self._dbconnector.commit()
        mycursor = self._dbconnector.cursor()
        mycursor.execute("SHOW TABLE STATUS")    
        tables = [iTable for iTable in mycursor]
        myTableLength = [i[10] for i in tables if i[0] == table_name][0]
        mycursor.close()
        return self.QueryData_From(table_name=table_name, row=myTableLength-rows, every=every, clean=clean)
    
    def stop(self):
        self._dbconnector.close()
    
    @property
    def all_tables_complete(self):
        return self._queryTables()
    
    @property
    def all_tables_names(self):
        return [iTableInfo[0] for iTableInfo in self._queryTables()]
    
    @property
    def latest_table(self):
        return self._selectLatestTable(self.all_tables_complete)
    
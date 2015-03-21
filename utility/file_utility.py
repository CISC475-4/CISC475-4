#!/usr/bin/env python2

"""
Source code in FileUtility.py regards reading the data from a structured CSV file into memory

This accounts for the step between raw data and storage in the database
"""
#TODO: multithreading with python threading library

import xlrd
import sys
import datetime

from time import time
from re import sub


class DataSet(object):
    """
    DataSet object represents all data points from an XLS worksheet

    Data - A dictionary of columns (String) with all corresponding data types (List of values)
        Keys - individual columns
        Values - A list of values in index order of the instances from the spreasheet
                 all data points for instance i can be found at Data.Keys(x)[i] 
                 for all xeX where X is the set of off Keys in the the dictionary, Data
    """

    #TODO: add metadata for each related instance 
    def __init__(self, column=[]):
        self.Data = {}
        for i in range(0,len(column)):
            self.Data[column[i]] = [] #instances should be added individually


    def __repr__(self):
        return str(self.Data)


    def add_instance(self, columns, values):
        """
        columns - to ensure the data is placed in the correct list
        values - list of values to columns
        add_datapoint adds a new data instances to the end of the Data.values list corresponding to the same data column (from input)
        """
        for i in range(0,len(columns)):
            self.Data[columns[i]].append(values[i])

    def get_instance_at(self, index):
        """
        retrieves in dictionary representation an instance at a give index
        """
        if index >= len(self.Data.values()[0]):
            print >> sys.stderr, "DataSet.get_instance_at(%d): no such instance" % (index)
            return 

        instance = {}
        for key in self.Data:
            instance[key] = self.Data[key][index]
        return instance
        

    def dataset_to_database(self, database):
        """
        pushes the whole dataset into the database
        """
        pass

def get_data_from(path):

    """
    reads in data from csv and adds instances to a DataSet object. Returns the created object
    """
    dataset = None

    try:
        with open(str(path), 'r') as dataFile:
            columns = dataFile.readline().strip().split(',')
            #deal with duplicates once, before creating a dictionary 
            for i in range(0,len(columns)):
                if columns[i] in columns[i+1:]: #append index as a unique identifier
                    columns[i] = columns[i] + "_" + str(i)

            dataset = DataSet(columns)
            for nextLine in dataFile: 
                data_points = nextLine.strip().split(',')
                dataset.add_instance(columns, data_points)
    except IOError:
        print >> sys.stderr, "Unable to open file at %s" % (path)

    return dataset


def xls_to_csv(path):
    """
    Convert all spreadsheets in file 'path' to a csv. Saved file is named w/ concatenation of path & spreadsheet name
    NOTE: input MUST be in '.xls' or '.xlsx' format

    Returns the pathname of each created file
    """
    names = [] #for return

    try:
        with xlrd.open_workbook(path) as wb:
            n = wb.nsheets #worksheets 
            # convert each sheet in wb to its own csv
            for i in range(0, n):
                doc = wb.sheet_by_index(i) #current worksheet
                r = doc.nrows #rows
 
                csv = open(sub('\.xls[x]$','',path) + doc.name + '.csv', 'w')
                names.append(str(csv.name)) #for return
            
                for j in range(0, r):
                    row_str = ""

                    for cell in doc.row_values(j):
                    #need to change the values from floats to match the original data
                        if type(cell) == float and cell % 1 == 0:
                            cell = int(cell)
                        row_str += str(cell) + ','

                    #remove trailing ',' and write
                    csv.write(row_str[0:len(row_str)-2] + '\n')
            
                wb.unload_sheet(i)
                csv.close()
    except IOError:
        print >> sys.stderr, "Unable to open file at %s" % (path)
        return 

    return tuple(names)

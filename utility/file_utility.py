#!/usr/bin/env python2

"""
Source code in FileUtility.py regards reading the data from a structured CSV file into memory

This accounts for the step between raw data and storage in the database
"""
#TODO: multithreading with python threading library

import xlrd
import sys

from time import time
from re import sub, findall
from os import path as ospath


class DataSet(object):
    """
    DataSet object represents all data points from an XLS worksheet

    Data - A dictionary of columns (String) with all corresponding data types (List of values)
        Keys - individual columns
        Values - A list of values in index order of the instances from the spreasheet
                 all data points for instance i can be found at Data.Keys(x)[i] 
                 for all xeX where X is the set of off Keys in the the dictionary, Data
    file_name - name of the file
    sheet_name - name of the sheet of origin
    TODO: sheet_function - type of data (either 'time series' or 'group')
    time_accessed - time the file was opened to create the dataset
    total_rows - number of data instances (rows in spreedsheet)
    child_id - the child the data corresponds to
    session_id - the session the data corresponds to
    """
    def __init__(self, column, file_name, sheet_name, sheet_function, time_accessed, total_rows, child_id, session_id):
        self.Data = {}
        for i in range(0,len(column)):
            self.Data[column[i]] = [] #instances should be added individually

        self.file_name = file_name
        self.sheet_name = sheet_name
        self.sheet_fuction = sheet_function
        self.time_accessed = time_accessed
        self.total_rows = total_rows
        self.child_id = child_id
        self.session_id = session_id


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
        returns in dictionary representation an instance at a give index
        """
        instance = {}
        for key in self.Data:
            instance[key] = self.Data[key][index]
        return instance


    def get_next_instance(self):
        """
        generator function for retrieving data instances
        """
        for i in range(0, self.total_rows): 
            yield self.get_instance_at(i)
        

    def dataset_to_database(self, database):
        """
        pushes the whole dataset into the database
        """
        pass


def get_data_from_xls(path):
    """
    bypasses the step of converting an XLS spreedsheet into a CSV. Data is loaded to memory directly from the given XLS spreedsheet.
    """
    datasets = [] 
    
    try:
        with xlrd.open_workbook(path) as wb: 
            access_time = time()
            file_name = ospath.basename(path)
            ids = parse_filename(file_name)

            num_worksheets = wb.nsheets

            for i in range(0, num_worksheets): 
                doc = wb.sheet_by_index(i) #current workbook, loads to a single dataset object
                rows = doc.nrows #includes the header in count. (Disclude for dataset instantiation)

                columns = uniqify_list([str(cell) for cell in doc.row_values(0)])

                dataset = DataSet(columns,file_name,doc.name,doc.name,access_time,rows-1,ids[0],ids[1])
                #TODO: above, get correct sheet function 

                for j in range(1, rows): 
                    next_row = doc.row_values(j) 
                    instance = []
                    for cell in next_row: 
                        if type(cell) == float and cell %1 == 0:
                            cell = int(cell)
                        instance.append(str(cell))
                    dataset.add_instance(columns, instance) 
                datasets.append(dataset)
    except IOError: 
        print >> sys.stderr, "Unable to open file at %s" % (path)
        return 

    return tuple(datasets) 
        

def get_data_from_csv(path):

    """
    reads in data from csv and adds instances to a DataSet object. Returns the created object
    """
    dataset = None

    try:
        with open(str(path), 'r') as dataFile:
            access_time = time()
            file_name = ospath.basename(path)
            ids = parse_filename(file_name)

            #deal with duplicates once, before creating a dictionary 
            columns = uniqify_list(dataFile.readline().strip().split(','))
            rows = 1

            dataset = DataSet(columns,file_name,file_name,file_name,access_time,rows,ids[0],ids[1])
            for nextLine in dataFile: 
                data_points = nextLine.strip().split(',')
                dataset.add_instance(columns, data_points)
                rows += 1
            dataset.total_rows = rows
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


def uniqify_list(str_list):
    """
    give duplicate elemnts in a list of string a unique name by appending it's index in the list
    """ 
    for k in range(0,len(str_list)):
        if str_list[k] in str_list[k+1:]:#append index as a unique identifier
            str_list[k] = str_list[k]+'_'+str(k)

    return str_list


def parse_filename(filename):
    """
    parses a given string filename for the CHILD ID and SESSION ID
    format:
        Output_[0-9]+_Training_D[0-9]+.{csv,xls(x)}
               ======           ======
               CHILD_ID         SESSION_ID
    (change code here as the excel format changes)
    """
    ids = findall('[0-9]+', filename)
    if len(ids) != 2:
        print >> sys.stderr, "unexpected filename"
        return 

    return tuple(ids) #CHILD_ID, SESSION_ID
    

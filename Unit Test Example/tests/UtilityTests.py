import sys
sys.path.append("../../Utility")

import FileUtility
from nose.tools import (assert_raises, assert_tuple_equal, assert_list_equal)

#test XLStoCSV
good_fn = "UtilityTestData_.xlsx"
fake_fn = "lego_building_block_chart.xlsx"

def test_XLStoCSV():
    print "testing XLStoCSV in FileUtility.py"
    #assert_raises(IOError, FileUtility.XLStoCSV, fake_fn)
    assert_tuple_equal(FileUtility.XLStoCSV(good_fn), ('UtilityTestData_AllGroupData.csv', 'UtilityTestData_TimeSeriesData.csv'))


#test getDataFrom
good_csv = "UtilityTestData_TimeSeriesData.csv"
fake_csv = "chromatic_lego_color_chart_by_time_of_day.csv"

timeSeriesHeader = ['TIME [SEC]', 'BEHAV 1', 'BEHAV 1 LEVEL', 'BEHAV 2', 'BEHAV 2 LEVEL', 'BEHAV 3', 'BEHAV 3 LEVEL', 'COMBO', 'COMBO LEVE']
timeSeriesValues = [{'TIME [SEC]': '0.333333333333', 'BEHAV 3': 'Ver_(quiet)', 'BEHAV 2': 'Aff_(interest)', 'BEHAV 1': 'Att_(trainer)', 'BEHAV 2 LEVEL': '3', 'BEHAV 3 LEVEL': '0', 'BEHAV 1 LEVEL': '5', 'COMBO': 'Att_(trainer):Aff_(interest):Ver_(quiet)', 'COMBO LEVE': '53'}]

def test_getDataFrom():
   print "testing getDataFrom in FileUtility.py"
   #assert_raises(IOError, FileUtility.getDataFrom, fake_csv)
   testRetrieval  = FileUtility.getDataFrom(good_csv)
   assert_list_equal(testRetrieval[0], timeSeriesHeader)
   assert_list_equal(testRetrieval[1], timeSeriesValues)

test_XLStoCSV()
test_getDataFrom()
